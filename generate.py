import os
import html

def generate_file_list(base_dir="."):
    file_entries = []

    for root, dirs, files in os.walk(base_dir):
        for name in files:
            # Relative path from base_dir
            rel_path = os.path.relpath(os.path.join(root, name), base_dir)
            file_entries.append(rel_path)

    return sorted(file_entries)

def generate_html(file_entries, output_file="index.html"):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n<html>\n<head>\n")
        f.write("<meta charset='utf-8'>\n<title>Directory Listing</title>\n")
        f.write("""
        <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background: #f4f4f4; }
        tr:nth-child(even) { background: #f9f9f9; }
        a { text-decoration: none; color: #0066cc; }
        a:hover { text-decoration: underline; }
        </style>
        """)
        f.write("</head>\n<body>\n")
        f.write("<h1>Directory Listing</h1>\n")
        f.write("<table>\n<tr><th>File</th><th>Type</th></tr>\n")

        for entry in file_entries:
            ext = os.path.splitext(entry)[1].lower() or "Other"
            safe_entry = html.escape(entry)
            f.write(f"<tr><td><a href='{safe_entry}'>{safe_entry}</a></td><td>{ext}</td></tr>\n")

        f.write("</table>\n</body>\n</html>")

if __name__ == "__main__":
    files = generate_file_list(".")
    generate_html(files)
    print("✅ index.html generated successfully.")

