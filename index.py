import os
import html

def generate_html_page():
    # Get the current working directory
    current_dir = os.getcwd()
    
    # List to store file information
    files_list = []

    # Scan the current directory for HTML and PDF files
    for root, _, files in os.walk(current_dir):
        for file in files:
            if file.endswith('.html') or file.endswith('.pdf'):
                # Get the relative path
                relative_path = os.path.relpath(os.path.join(root, file), current_dir)
                files_list.append(relative_path)

    # Start building the HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Files in {current_dir}</title>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        a {{ color: blue; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>HTML and PDF Files in the Current Folder</h1>
    <table>
        <tr>
            <th>File Name</th>
            <th>Link</th>
        </tr>"""

    # Populate the table with files
    for file in files_list:
        html_content += f"""
        <tr>
            <td>{html.escape(file)}</td>
            <td><a href="{html.escape(file)}" target="_blank">Open</a></td>
        </tr>"""

    # Closing HTML tags
    html_content += """
    </table>
</body>
</html>
"""

    # Write the HTML content to a file
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    print("HTML page 'index.html' has been created in the current folder.")

if __name__ == "__main__":
    generate_html_page()

