from __future__ import annotations

from dotenv import load_dotenv

load_dotenv()

import json
import os
from pathlib import Path
from typing import Dict, Optional, Tuple

import requests
from markdown import markdown

CONFLUENCE_API_URL = os.getenv("CONFLUENCE_API_URL", "").rstrip("/")
CONFLUENCE_USER = os.getenv("CONFLUENCE_USER", "")
CONFLUENCE_TOKEN = os.getenv("CONFLUENCE_TOKEN", "")

# Optional: explicitly target a space (recommended for CI)
CONFLUENCE_SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")  # e.g. "INTPREP"
CONFLUENCE_SPACE_NAME = os.getenv("CONFLUENCE_SPACE_NAME")  # e.g. "Interview Prep"

IGNORED_TITLES = {"overview", "getting started in confluence"}

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
PAGE_MAP_PATH = REPO_ROOT / "confluence_sync" / "page_map.json"


def _auth() -> Tuple[str, str]:
    if not (CONFLUENCE_API_URL and CONFLUENCE_USER and CONFLUENCE_TOKEN):
        raise RuntimeError(
            "Missing Confluence environment variables. "
            "Please set CONFLUENCE_API_URL, CONFLUENCE_USER, CONFLUENCE_TOKEN."
        )
    return CONFLUENCE_USER, CONFLUENCE_TOKEN


def _request(method: str, url: str, **kwargs) -> requests.Response:
    """
    Wrapper to provide consistent errors for common auth failures.
    """
    res = requests.request(method, url, auth=_auth(), timeout=60, **kwargs)
    if res.status_code in (401, 403):
        raise RuntimeError(
            f"Confluence API auth failed ({res.status_code}). "
            "Your token may be expired/revoked or lacks permissions."
        )
    res.raise_for_status()
    return res


def fetch_personal_space_key() -> str:
    """
    Fetch the personal space key for the authenticated user (Confluence Cloud).
    """
    url = f"{CONFLUENCE_API_URL}/space"
    res = _request("GET", url)
    data = res.json()
    for space in data.get("results", []):
        if space.get("type") == "personal":
            return space["key"]
    raise RuntimeError("Personal space key not found. Set CONFLUENCE_SPACE_KEY explicitly.")


def space_exists(space_key: str) -> bool:
    url = f"{CONFLUENCE_API_URL}/space/{space_key}"
    res = requests.get(url, auth=_auth(), timeout=60)
    if res.status_code == 404:
        return False
    if res.status_code in (401, 403):
        raise RuntimeError(
            f"Confluence API auth failed ({res.status_code}). "
            "Your token may be expired/revoked or lacks permissions."
        )
    res.raise_for_status()
    return True


def try_create_space(space_key: str, space_name: str) -> bool:
    """
    Attempt to create a Confluence space (requires admin/global permissions).
    If Confluence denies, we return False and let caller fallback.
    """
    url = f"{CONFLUENCE_API_URL}/space"
    payload = {
        "key": space_key,
        "name": space_name,
        "type": "global",
    }
    res = requests.post(url, auth=_auth(), json=payload, timeout=60)
    if res.status_code in (200, 201):
        print(f"✅ Created Confluence space '{space_key}'")
        return True
    # Permission issues are common here; don't hard fail.
    if res.status_code in (401, 403):
        print(
            f"⚠️ Could not create space '{space_key}' (permission denied). "
            "Falling back to your personal space."
        )
        return False
    if res.status_code == 400:
        # Already exists or invalid key format
        return False
    try:
        print(f"⚠️ Could not create space '{space_key}'. Status={res.status_code}. Body={res.text[:300]}")
    except Exception:
        pass
    return False


def get_target_space_key() -> str:
    """
    Decide which space to use:
    - If CONFLUENCE_SPACE_KEY is provided: use it (create if missing and possible).
    - Else: use the authenticated user's personal space.
    """
    if CONFLUENCE_SPACE_KEY:
        desired = CONFLUENCE_SPACE_KEY
        if space_exists(desired):
            return desired
        # If missing, try to create it (admin permission required)
        name = CONFLUENCE_SPACE_NAME or desired
        created = try_create_space(desired, name)
        if created and space_exists(desired):
            return desired
        # Fallback
        return fetch_personal_space_key()
    return fetch_personal_space_key()


def fetch_all_pages(space_key: str) -> Dict[str, str]:
    """
    Return {Title: PageId} for all pages in a space.
    """
    pages: Dict[str, str] = {}
    start = 0
    limit = 50
    while True:
        url = f"{CONFLUENCE_API_URL}/content"
        params = {
            "spaceKey": space_key,
            "type": "page",
            "expand": "title",
            "limit": limit,
            "start": start,
        }
        res = _request("GET", url, params=params)
        data = res.json()

        for page in data.get("results", []):
            title = (page.get("title") or "").strip()
            if title.strip().lower() in IGNORED_TITLES:
                continue
            pages[title] = page["id"]

        if len(data.get("results", [])) < limit:
            break
        start += limit

    return pages


def read_title_and_body_from_md(md_path: Path) -> Tuple[str, str]:
    """
    Title priority:
      1) First Markdown H1: '# Title'
      2) Filename (excel.md -> Excel)
    Body:
      - Entire markdown converted to HTML (Confluence storage format)
    """
    text = md_path.read_text(encoding="utf-8")
    first_line = (text.splitlines()[0].strip() if text.splitlines() else "")
    if first_line.startswith("# "):
        title = first_line[2:].strip()
    else:
        title = md_path.stem.replace("_", " ").replace("-", " ").title()

    html_body = markdown(text)
    return title, html_body


def create_page(space_key: str, title: str, html_body: str, parent_id: Optional[str] = None) -> str:
    """
    Create a new Confluence page in the given space. Returns page_id.
    """
    url = f"{CONFLUENCE_API_URL}/content"
    payload = {
        "type": "page",
        "title": title,
        "space": {"key": space_key},
        "body": {"storage": {"value": html_body, "representation": "storage"}},
    }
    if parent_id:
        payload["ancestors"] = [{"id": parent_id}]

    res = _request("POST", url, json=payload, headers={"Content-Type": "application/json"})
    page_id = res.json()["id"]
    print(f"🆕 Created page: '{title}' (id={page_id})")
    return page_id


def ensure_pages_from_docs(space_key: str, existing_pages: Dict[str, str]) -> Dict[str, str]:
    """
    If Confluence is empty (or page_map.json is empty), bootstrap Confluence from docs/*.md:
      - For each docs/*.md: create the page if it doesn't exist
      - Return an updated mapping (existing + created)
    """
    if not DOCS_DIR.exists():
        print(f"⚠️ Docs dir not found: {DOCS_DIR}")
        return existing_pages

    updated = dict(existing_pages)

    md_files = sorted(DOCS_DIR.glob("*.md"))
    if not md_files:
        print("⚠️ No markdown files found in docs/. Nothing to bootstrap.")
        return updated

    for md_file in md_files:
        title, html_body = read_title_and_body_from_md(md_file)

        if title.strip().lower() in IGNORED_TITLES:
            print(f"⏭️ Skipping ignored markdown: {md_file.name}")
            continue

        # Confluence titles are case-sensitive in API results; try exact match first,
        # then a case-insensitive scan.
        page_id = updated.get(title)
        if not page_id:
            for existing_title, existing_id in updated.items():
                if existing_title.strip().lower() == title.strip().lower():
                    page_id = existing_id
                    title = existing_title  # preserve canonical title
                    break

        if page_id:
            continue

        # Create from scratch
        created_id = create_page(space_key, title, html_body)
        updated[title] = created_id

    return updated


def save_page_map(mapping: Dict[str, str]) -> None:
    PAGE_MAP_PATH.parent.mkdir(parents=True, exist_ok=True)
    PAGE_MAP_PATH.write_text(json.dumps(mapping, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Saved page_map.json with {len(mapping)} pages -> {PAGE_MAP_PATH}")


def load_existing_page_map() -> Dict[str, str]:
    if not PAGE_MAP_PATH.exists():
        return {}
    try:
        return json.loads(PAGE_MAP_PATH.read_text(encoding="utf-8") or "{}")
    except Exception:
        return {}


if __name__ == "__main__":
    try:
        space_key = get_target_space_key()
        confluence_pages = fetch_all_pages(space_key)

        # If the map is empty or Confluence is empty, bootstrap from docs/
        existing_map = load_existing_page_map()
        if not existing_map or not confluence_pages:
            print("ℹ️ Bootstrapping Confluence pages from docs/ because page_map.json or space is empty.")
            confluence_pages = ensure_pages_from_docs(space_key, confluence_pages)

        save_page_map(confluence_pages)
    except Exception as e:
        print(f"❌ Failed: {e}")
