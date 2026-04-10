import os
from pathlib import Path
from html import escape

# ---------------- CONFIG ----------------
ROOT_DIR = Path(".")  # change this if needed
OUTPUT_FILE = "index.html"
# ----------------------------------------


def generate_html_for_directory(dir_path):
    """Generate HTML content recursively for a directory."""

    def folder_to_html(folder_path):
        items_html = ""
        for entry in sorted(folder_path.iterdir()):
            if entry.is_dir():
                # Recursive dropdown for subfolder
                sub_html = folder_to_html(entry)
                items_html += f"""
                <div class="folder-card">
                    <button class="dropdown-btn">{escape(entry.name)}</button>
                    <div class="dropdown-container">
                        {sub_html}
                    </div>
                </div>
                """
            else:
                # File link
                items_html += f'<div class="file-item"><a href="{escape(entry.name)}">{escape(entry.name)}</a></div>'
        return items_html

    folder_html = folder_to_html(dir_path)

    # HTML Template
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Index of {escape(str(dir_path))}</title>
<style>
body {{
  font-family: Arial, sans-serif;
  background: #f5f5f5;
  padding: 20px;
}}
.folder-card {{
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  padding: 15px;
  margin: 10px 0;
}}
.dropdown-btn {{
  background: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 15px;
  width: 100%;
  text-align: left;
  font-size: 16px;
  cursor: pointer;
}}
.dropdown-btn:hover {{
  background: #0056b3;
}}
.dropdown-container {{
  display: none;
  margin-top: 10px;
  padding-left: 20px;
}}
.file-item {{
  padding: 5px 0;
}}
a {{
  text-decoration: none;
  color: #333;
}}
a:hover {{
  color: #007bff;
}}
</style>
</head>
<body>
<h2>📁 Index of {escape(str(dir_path))}</h2>
{folder_html}

<script>
document.querySelectorAll(".dropdown-btn").forEach(btn => {{
  btn.addEventListener("click", () => {{
    const container = btn.nextElementSibling;
    container.style.display = container.style.display === "block" ? "none" : "block";
  }});
}});
</script>
</body>
</html>
"""
    return html


def create_index_recursively(base_dir):
    """Recursively create index.html for all folders."""
    for root, dirs, files in os.walk(base_dir):
        root_path = Path(root)
        html_content = generate_html_for_directory(root_path)
        index_path = root_path / OUTPUT_FILE
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"✅ Created index for: {root_path}")


if __name__ == "__main__":
    create_index_recursively(ROOT_DIR)
    print("\nAll folder index files generated successfully!")

