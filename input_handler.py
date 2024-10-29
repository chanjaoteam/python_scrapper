import re

def prompt_for_url():
    """Prompt the user for a product listing URL and validate it."""
    url_pattern = re.compile(
        r'^(https?://)?(www\.)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})(/[^\s]*)?$'
    )
    while True:
        url = input("Please enter the product listing URL: ")
        # if url_pattern.match(url):
        return url
        # else:
        #     print("Invalid URL format. Please try again.")
