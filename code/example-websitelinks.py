# trying another link to get urls
# Define the base URL
base_url = "https://medlineplus.gov/ency/encyclopedia_{}.htm"

# Open a file in append mode
with open("output_urls2.txt", "w", encoding="utf-8") as file:
    # Iterate over the letters from 'A' to 'Z'
    for letter in range(ord('A'), ord('Z') + 1):
        letter_url = base_url.format(chr(letter))

        # Fetch HTML content
        html_text = requests.get(
            letter_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            }
        ).content.decode()

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html_text, 'html.parser')

        # Find the ul tag with id="index"
        index_ul = soup.find('ul', id='index')

        # Check if the ul tag is found
        if index_ul:
            # Find all li tags under the ul
            li_tags = index_ul.find_all('li')

            for li_tag in li_tags:
                # Find the anchor tag under li
                a_tag = li_tag.find('a')

                # Check if the anchor tag is found and has an href attribute
                if a_tag and 'href' in a_tag.attrs:
                    href_value = a_tag['href']
#                     print(href_value)
                    file.write("https://medlineplus.gov/ency/" + href_value + "\n")
