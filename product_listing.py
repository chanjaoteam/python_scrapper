from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from db_manager import DatabaseManager
import time

class ProductListing:
    def __init__(self, driver):
        self.driver = driver
        self.db_manager = DatabaseManager()

    def scrape_listings(self, url):
        """Scrape product listing pages and manage pagination."""
        self.driver.get(url)
        time.sleep(2)  # Wait for the page to load

        page_html = self.driver.execute_script("return document.body.innerHTML;")

        all_links = self.driver.find_elements(By.TAG_NAME, 'a')

        # Check for pagination links
        pagination_links = []
        for link in all_links:
            href = link.get_attribute('href')
            if href:
                # Check for common pagination keywords
                if (any(keyword in href.lower() for keyword in ["next", "previous", "pagination"]) or ("page" in href.lower() and href.lower().find("page") > 0)):
                    pagination_links.append(href)

        # Check for infinite scroll
        load_more_button = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Load more')]")  # For button
        load_more_link = self.driver.find_elements(By.XPATH, "//a[contains(text(), 'Load more')]")  # For anchor link

        infinite_scroll = bool(load_more_button or load_more_link)

        print(pagination_links.__len__)

        # Output results
        if pagination_links:
            print("Pagination Links Found:")
            for link in pagination_links:
                print(link)
        else:
            print("No pagination links found. Infinite scroll detected.")
            if infinite_scroll:
                if bool(load_more_button):
                    print("Load more button found, indicating infinite scroll.")
                else:
                    print("Load more link found, indicating infinite scroll.")
            else:
                print("No load more button found, and no pagination links detected.")


        self.db_manager.insert_record('list_page',{"html_content": page_html,})

        while True:
            # Extract product listings
            products = self.driver.find_elements(By.CLASS_NAME, 'product-item')
            for product in products:
                # self.db_manager.create_connection()
                self.db_manager.insert_record('products_in_list',{"name": "",})
                # Store the HTML content in the database
                # Placeholder for actual database insertion logic

            # Check for next page
            try:
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@class='next']"))
                )
                next_button.click()
                time.sleep(2)  # Wait for the next page to load
            except Exception:
                print("No more pages to scrape.")
                break
