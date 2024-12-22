import os

def generate_html(directory, output_file="index.html"):
    # Helper function to create HTML content recursively
    def build_html(dir_path, base_path):
        html = "<ul>\n"
        for item in sorted(os.listdir(dir_path)):
            full_path = os.path.join(dir_path, item)
            relative_path = os.path.relpath(full_path, base_path)
            if os.path.isdir(full_path):
                # Recursive call for subdirectories
                html += f'<li><b>{item}/</b>{build_html(full_path, base_path)}</li>\n'
            else:
                # Create clickable link for files
                html += f'<li><a href="{relative_path}" target="_blank">{item}</a></li>\n'
        html += "</ul>\n"
        return html

    # Generate the main HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>File Explorer</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            ul {{ list-style-type: none; }}
            a {{ text-decoration: none; color: blue; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <h1>File Explorer</h1>
        {build_html(directory, directory)}
    </body>
    </html>
    """

    # Write the HTML content to the output file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"HTML file generated: {output_file}")

# Directory to scan
directory_to_scan = "./"  # Change to your desired folder
output_html_file = "file_explorer.html"

# Generate the HTML file
generate_html(directory_to_scan, output_html_file)

