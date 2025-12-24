from __future__ import annotations

from dotenv import load_dotenv

load_dotenv()

import os
import requests


def _die(msg: str, code: int = 2) -> None:
    print(msg)
    raise SystemExit(code)


def _auth() -> tuple[str, str]:
    api_url = os.getenv("CONFLUENCE_API_URL", "").rstrip("/")
    user = os.getenv("CONFLUENCE_USER", "")
    token = os.getenv("CONFLUENCE_TOKEN", "")
    if not api_url:
        _die("❌ Missing env var: CONFLUENCE_API_URL (e.g., https://<site>.atlassian.net/wiki/rest/api)")
    if not user:
        _die("❌ Missing env var: CONFLUENCE_USER (your Confluence/Atlassian email)")
    if not token:
        _die("❌ Missing env var: CONFLUENCE_TOKEN (API token / PAT). Update your GitHub Secret.")
    return user, token


def _request(url: str) -> requests.Response:
    user, token = _auth()
    return requests.get(url, auth=(user, token), timeout=60)


def main() -> None:
    api_url = os.getenv("CONFLUENCE_API_URL", "").rstrip("/")
    space_key = os.getenv("CONFLUENCE_SPACE_KEY", "").strip()

    # 1) Check token/auth (fast fail)
    # Confluence Cloud typically supports /user/current; if not, fall back to /space?limit=1.
    auth_ok = False
    tried = []

    for path in ("/user/current", "/space?limit=1"):
        url = f"{api_url}{path}"
        tried.append(url)
        try:
            res = _request(url)
        except Exception as e:
            _die(f"❌ Confluence health check failed while calling {url}: {e}")

        if res.status_code in (401, 403):
            _die(
                "❌ Confluence authentication failed (HTTP %s).\n"
                "Likely causes:\n"
                "- CONFLUENCE_TOKEN expired/revoked\n"
                "- Token/user mismatch\n"
                "- Token lacks permissions\n\n"
                "Fix: generate a new token and update the GitHub Secret CONFLUENCE_TOKEN."
                % res.status_code
            )

        if res.status_code == 404:
            # Try next path
            continue

        if 200 <= res.status_code < 300:
            auth_ok = True
            break

        _die(f"❌ Confluence health check got unexpected status {res.status_code} for {url}: {res.text[:200]}")

    if not auth_ok:
        _die(
            "❌ Could not verify Confluence API endpoints.\n"
            "Tried:\n- " + "\n- ".join(tried) + "\n\n"
            "Your CONFLUENCE_API_URL may be incorrect. It should usually end with /wiki/rest/api."
        )

    print("✅ Confluence auth looks good.")

    # 2) Check space reachability if a space key is provided
    if space_key:
        url = f"{api_url}/space/{space_key}"
        res = _request(url)

        if res.status_code == 404:
            print(
                f"⚠️ Space '{space_key}' not found. The sync will attempt to create it (requires permissions) "
                "or fall back to personal space depending on your scripts."
            )
            return

        if res.status_code in (401, 403):
            _die(
                f"❌ Auth ok, but cannot access space '{space_key}' (HTTP {res.status_code}).\n"
                "Your token/user may not have access to this space."
            )

        if 200 <= res.status_code < 300:
            print(f"✅ Space '{space_key}' is accessible.")
            return

        _die(f"❌ Unexpected status {res.status_code} while checking space '{space_key}': {res.text[:200]}")

    print("ℹ️ No CONFLUENCE_SPACE_KEY provided; using personal space behavior.")


if __name__ == "__main__":
    main()
