import requests
from bs4 import BeautifulSoup
from datetime import datetime

# URL of the page to download
url = "https://www.asianetnews.com/kerala-news"

# Get the current date and format it for the filename
date_str = datetime.now().strftime("%b_%d_%Y").lower()
filename = f"{date_str}.html"

# Fetch the HTML content of the page
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find all <a> tags with a title attribute
    a_tags = soup.find_all("a", title=True)
    
    # Start creating the HTML file content
    html_content = "<html><head><title>Asianet News Kerala</title></head><body>"
    html_content += "<h1>Asianet News Kerala - Links with Titles</h1><ul>"
    
    for tag in a_tags:
        title_text = tag['title'].strip()
        link_text = tag.get_text(strip=True)
        link_href = tag.get("href", "#")  # Use "#" if there's no href
        
        # Append each link with title and text to the HTML content
        html_content += f'<li><a href="{link_href}" title="{title_text}">{link_text}</a></li>'
    
    # Close the HTML tags
    html_content += "</ul></body></html>"
    
    # Write the content to an HTML file
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_content)
    
    print(f"HTML file created: {filename}")
else:
    print("Failed to retrieve the page.")

