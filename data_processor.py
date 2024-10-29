import openai
from config import OPENAI_KEY

class DataProcessor:
    def __init__(self):
        openai.api_key = OPENAI_KEY

    def process_html(self, html_content): 
        """Send HTML content to OpenAI API for processing."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": f"Extract product information from the following HTML: {html_content}"}
                ]
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
