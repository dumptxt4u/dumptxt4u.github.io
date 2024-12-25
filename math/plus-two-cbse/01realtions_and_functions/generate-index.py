import os

def generate_html(directory, output_file="index.html"):
    """
    Generates an HTML page listing all files in the directory and subdirectories as clickable links.

    Parameters:
        directory (str): The directory to scan.
        output_file (str): The name of the output HTML file.
    """
    html_content = [
        "<html>",
        "<head>",
        "    <title>Directory Listing</title>",
        "    <style>",
        "        body { font-family: Arial, sans-serif; }",
        "        a { text-decoration: none; color: blue; }",
        "        a:hover { text-decoration: underline; }",
        "        ul { list-style-type: none; padding-left: 1em; }",
        "    </style>",
        "</head>",
        "<body>",
        f"    <h1>Directory Listing for {os.path.abspath(directory)}</h1>",
        "    <ul>",
    ]

    for root, _, files in os.walk(directory):
        rel_root = os.path.relpath(root, directory)
        if rel_root != ".":
            html_content.append(f"<li><strong>{rel_root}/</strong></li>")
            html_content.append("<ul>")

        for file in files:
            file_path = os.path.join(root, file)
            rel_file_path = os.path.relpath(file_path, directory)
            html_content.append(
                f"        <li><a href=\"{rel_file_path}\" target=\"_blank\">{rel_file_path}</a></li>"
            )

        if rel_root != ".":
            html_content.append("</ul>")

    html_content.append("    </ul>")
    html_content.append("</body>")
    html_content.append("</html>")

    with open(output_file, "w") as f:
        f.write("\n".join(html_content))

    print(f"HTML file generated: {output_file}")

if __name__ == "__main__":
    directory_to_scan = input("Enter the directory to scan (leave blank for current directory): ") or "."
    output_file_name = input("Enter the output HTML file name (default: index.html): ") or "index.html"
    generate_html(directory_to_scan, output_file_name)

