# Install python-dotenv if needed
# pip install python-dotenv
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')
SCRAPING_URL = os.getenv('SCRAPING_URL')
SCRAPING_INTERVAL = int(os.getenv('SCRAPING_INTERVAL', 10))
TIMEOUT = int(os.getenv('TIMEOUT', 30))
OPENAI_KEY = os.getenv('OPENAI_KEY')
