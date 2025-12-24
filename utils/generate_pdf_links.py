import os
import re

PDF_DIR = "interview_questions"
README_FILE = "README.md"
SECTION_HEADER = "## 📥 Downloadable PDFs"
GITHUB_REPO = "https://github.com/TaranjyotS/interview-prep/raw/main/interview_questions"  # ✅ Replace if needed

def generate_pdf_section():
    pdf_files = sorted(f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf"))
    if not pdf_files:
        return ""

    lines = [f"{SECTION_HEADER}\n", "The following PDF resources are available for download:\n"]
    for file in pdf_files:
        title = os.path.splitext(file)[0].replace("_", " ").title()
        url = f"{GITHUB_REPO}/{file.replace(' ', '%20')}"  # Encode spaces for URLs
        lines.append(f"- <a href=\"{url}\">{title} (PDF)</a>")

    return "\n".join(lines)

def update_readme():
    if not os.path.exists(README_FILE):
        print("❌ README.md not found.")
        return

    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    new_section = generate_pdf_section()
    if not new_section:
        print("⚠️ No PDF files found. Skipping update.")
        return

    # Remove existing section if it exists
    pattern = re.compile(f"{SECTION_HEADER}.*?(?=\n## |\Z)", re.DOTALL)
    if re.search(pattern, content):
        content = re.sub(pattern, new_section, content)
    else:
        content = content.rstrip() + "\n\n" + new_section

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ README.md updated with clickable inline PDF links.")

if __name__ == "__main__":
    update_readme()
