import logging
import time
import random
import os
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import mysql.connector
from bs4 import BeautifulSoup

# Configure logging
log_file = 'scraper.log'
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TaobaoScraper:
    def __init__(self, products_limit=10, sleep_time=0):
        self.products_limit = products_limit
        self.sleep_time = sleep_time
        self.url = 'https://www.taobao.com/'
        self.store_name = 'taobao'
        self.user_profile_path = r"C:\Users\user\Documents\Projects\webscrapper_prompt_pj\scrapper_code\user_profile"
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36"
        ]

    def create_database_connection(self):
        logging.info("Connecting to MySQL database...")
        try:
            connection = mysql.connector.connect(
                host='db.chanjao.com',
                user='thihako',
                password='7QqZBUPxMaq8iBfG',
                database='supply_chain'
            )
            logging.info("Database connection established.")
            return connection
        except mysql.connector.Error as err:
            logging.error(f"Error connecting to database: {err}")
            raise

    def save_raw_html(self, filename, content):
        os.makedirs('raw_html', exist_ok=True)
        with open(f'raw_html/{filename}', 'w', encoding='utf-8') as f:
            f.write(content)
        logging.info(f"Saved raw HTML to {filename}")

    def scrape_product_info(self, product_name, headless=False, verbose=True):
        product_name = product_name.lower().replace(' ', '%20')
        search_url = f"https://xssyjt.1688.com/page/offerlist.htm?spm=0.0.wp_pc_common_topnav_38229151.0"
        if verbose: print(search_url)

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=headless)
            context = browser.new_context(user_agent=random.choice(self.user_agents))
            page = context.new_page()
            stealth_sync(page)

            # Introduce a random delay to mimic human behavior
            time.sleep(random.uniform(2, 5))
            page.goto(search_url)

            # Wait for a specific selector that appears when data is fully loaded
            try:
                page.wait_for_selector('.Card--doubleCardWrapper--L2XFE73', timeout=10000)  # Wait up to 10 seconds
            except Exception as e:
                logging.error(f"Timeout waiting for product cards: {e}")
                return []

            # Check for captcha
            if "Please slide to verify" in page.content() or "unusual traffic" in page.content():
                logging.error('Captcha detected!')
                print('Captcha detected! Please solve it manually.')
                input('Press Enter after solving the captcha to continue...')
                return []

            # Now that the page is fully loaded, get the HTML content
            source_code = page.content()
            self.save_raw_html('product_list.html', source_code)

            products = []
            items = page.query_selector_all('.Card--doubleCardWrapper--L2XFE73')
            for item in items:
                name = item.query_selector('.Title--title--jCOPvpf').text_content()
                price_int = item.query_selector('.Price--priceInt--ZlsSi_M').text_content()
                price_float = item.query_selector('.Price--priceFloat--h2RR0RK').text_content()
                merchant = item.query_selector('.ShopInfo--shopName--rg6mGmy').text_content()
                price = int(price_int.strip()) + float(price_float.strip())
                url = item.get_attribute('href')
                if not url.startswith('https:'):
                    url = 'https:' + url
                product = {"product_name": name.strip(), "price": price, "merchant": merchant.strip(), "url": url,
                        'platform': self.store_name}
                products.append(product)
                if len(products) == self.products_limit:  # Fix: use `products_limit` instead of `limit`
                    break

            browser.close()

        return products

    def insert_product_data(self, connection, product):
        cursor = connection.cursor()
        sql = """
        INSERT INTO products (name, price, merchant, raw_html_path)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (
            product['product_name'],
            product['price'],
            product['merchant'],
            'raw_html/product_list.html'  # Example path
        ))
        connection.commit()
        logging.info(f"Inserted product data: {product['product_name']}")

    def scrape_product_info_by_weight(self, product_name):
        product_info = self.scrape_product_info(product_name,True,True)
        if len(product_info) == 0:
            print('Possible captcha detected!')
            #exit()
        return product_info

def main():
    logging.info("Starting TaobaoScraper...")
    scraper = TaobaoScraper(products_limit=10, sleep_time=1)
    
    # Connect to the database
    connection = scraper.create_database_connection()
    
    products = scraper.scrape_product_info_by_weight("enzyme")
    
    # Insert product data into the database
    for product in products:
        scraper.insert_product_data(connection, product)

    logging.info("Scraping completed.")
    connection.close()

if __name__ == "__main__":
    main()
print("Logging setup complete. Check scraper.log for details.")
