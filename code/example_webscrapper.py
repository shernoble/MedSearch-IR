from bs4 import BeautifulSoup
import requests
import os

def extract_content(url):
    # Fetch HTML content
    html_text = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
    ).content.decode()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_text, 'html.parser')

    # Find the <div> with class "content" or "main-content"
    content_div = soup.find('div', class_='content')

    if content_div:
        # Exclude content from <div class="myc-subscription-form">

        # Extract content within <h1>, <h2>, <h3>, <h4>, <p>, <li>, and <span> tags within the modified content_div
        h1_tags = content_div.find_all('h1')
        h2_tags = content_div.find_all('h2')
        h3_tags = content_div.find_all('h3')
        h4_tags = content_div.find_all('h4')
        p_tags = content_div.find_all('p')
        li_tags = content_div.find_all('li')
        span_tags = content_div.find_all('span')
    
        return {
            'url': url,
            'h1_tags': h1_tags,
            'h2_tags': h2_tags,
            'h3_tags': h3_tags,
            'h4_tags': h4_tags,
            'p_tags': p_tags,
            'li_tags': li_tags,
            'span_tags': span_tags
        }
    else:
        print(f"No content <div class='content'> or <div class='main-content'> found in {url}")
        return None

# Read the list of URLs from a text file
with open("temp_urls.txt", "r") as file:
    urls = file.readlines()

# Specify the folder to store output files
output_folder = "output_files"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Iterate through each URL
for url in urls:
    # url = url.strip()  # Remove leading/trailing whitespaces and newlines

    # Check if the URL belongs to the specified domain
    if url.startswith("https://www.news-medical.net//news"):
        # Extract content for the current URL
        content = extract_content(url)

        if content:
            # Create a new file for each URL in the output folder
            file_path = os.path.join(output_folder, f"{url.replace('/', '_').replace(':', '_')}.txt")

            # Write the extracted content to the output file
            with open(file_path, "w", encoding="utf-8") as file_out:
                file_out.write(f"URL: {url}\n")

                # Write content of each tag type to the output file
                for tag_type in ['h1_tags', 'h2_tags', 'h3_tags', 'h4_tags', 'p_tags', 'li_tags', 'span_tags']:
                    tags = content[tag_type]
                    # file_out.write(f"\n--- {tag_type} ---\n")
                    for tag in tags:
                        file_out.write(f"{tag.text}\n")
