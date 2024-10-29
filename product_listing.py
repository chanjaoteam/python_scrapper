from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from db_manager import DatabaseManager
from dynamic_content_handler import DynamicContentHandler
import time

class ProductListing:
    def __init__(self, driver):
        self.driver = driver
        self.db_manager = DatabaseManager()
        self.dynamic_content_handler = DynamicContentHandler(driver)

    def scrape_listings(self, url):
        """Scrape product listing pages and manage pagination."""
        self.driver.get(url)
        time.sleep(2)  # Initial wait for the page to load

        # Store the current page's HTML content
        self.store_html_content()

        # Scrape products on the current page
        self.extract_products()

        while True:
            if not self.handle_pagination():
                print("No more pages or products to scrape.")
                break

    def store_html_content(self):
        """Store the current HTML content of the page with retries."""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                page_html = self.driver.execute_script("return document.body.innerHTML;")
                # Store or process the page_html as needed
                return
            except Exception as e:
                print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
                time.sleep(1)  # Wait before retrying
        print("Failed to store HTML content after multiple attempts.")

    def extract_products(self):
        """Extract product names from the current page."""
        products = self.driver.find_elements(By.CLASS_NAME, 'product-item')
        for product in products:
            try:
                product_name = product.find_element(By.CLASS_NAME, 'product-name').text  # Adjust class name as needed
                self.db_manager.insert_record('products_in_list', {"name": product_name})
            except Exception as e:
                print(f"Error extracting product name: {e}")

    def handle_pagination(self):
        """Handle pagination for both dynamic and static content."""
        if self.is_infinite_scroll():
            return self.handle_infinite_scroll()
        else:
            return self.handle_static_pagination()

    def is_infinite_scroll(self):
        """Check for the presence of infinite scroll."""
        load_more_button = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Load more')]")
        load_more_link = self.driver.find_elements(By.XPATH, "//a[contains(text(), 'Load more')]")
        return bool(load_more_button or load_more_link)

    def handle_infinite_scroll(self):
        """Click 'Load more' buttons or links if present."""
        load_more_button = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Load more')]")
        load_more_link = self.driver.find_elements(By.XPATH, "//a[contains(text(), 'Load more')]")
        
        if load_more_button:
            try:
                load_more_button[0].click()  # Click the button
                time.sleep(2)  # Wait for the new products to load
                self.extract_products()  # Extract newly loaded products
                return True
            except Exception as e:
                print(f"Error clicking load more button: {e}")
                return False
        elif load_more_link:
            try:
                load_more_link[0].click()  # Click the link
                time.sleep(2)  # Wait for the new products to load
                self.extract_products()  # Extract newly loaded products
                return True
            except Exception as e:
                print(f"Error clicking load more link: {e}")
                return False
        else:
            print("No more products to load.")
            return False  # No more products to load

    def handle_static_pagination(self):
        """Navigate to the next page using static pagination links."""
        
            # Locate and click the "Next" button using the updated XPath
        
        next_button = self.dynamic_content_handler.wait_for_element("//button[contains(text(), '下一页')]")
        try:
            next_button.click()
            self.store_html_content()  # Store the new page's HTML content
            self.extract_products()  # Extract products from the new page
            return True
        except Exception as e:
            print(f"Error navigating to the next page in static: {e}")
            print("Attempting to scrape pagination links dynamically...")
            return self.dynamic_scrape_pagination()

    def dynamic_scrape_pagination(self):
        """Dynamically scrape pagination links if static links fail."""
        try:
            # Wait for pagination links to appear
            self.dynamic_content_handler.wait_for_elements("//div[contains(@style, 'height: 38px;')]")
            
            pagination_links = self.driver.find_elements(By.XPATH, "//div[contains(@style, 'height: 38px;')]")
            for link in pagination_links:
                # Check if the link represents the next page
                if link.text == "下一页":
                    link.click()
                    time.sleep(2)  # Wait for the next page to load
                    self.store_html_content()  # Store the new page's HTML content
                    self.extract_products()  # Extract products from the new page
                    return True
            print("No pagination links found.")
            return False
        except Exception as e:
            print(f"Error during dynamic pagination scraping: {e}")
            return False  # No more pages to scrape
