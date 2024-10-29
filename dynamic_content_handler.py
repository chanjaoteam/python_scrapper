from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DynamicContentHandler:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, xpath, timeout=300):
        """Wait for a specific element to load on the page."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except Exception as e:
            print(f"Error waiting for element: {xpath}. Exception: {e}")

    def wait_for_elements(self, xpath, timeout=300):
        """Wait for multiple elements to load on the page."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath))
            )
        except Exception as e:
            print(f"Error waiting for elements: {xpath}. Exception: {e}")

    def click_element(self, xpath, timeout=300):
        """Wait for an element to be clickable and then click it."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
        except Exception as e:
            print(f"Error clicking element: {xpath}. Exception: {e}")

    def get_element_text(self, xpath, timeout=300):
        """Wait for an element to load and return its text."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return element.text
        except Exception as e:
            print(f"Error getting text from element: {xpath}. Exception: {e}")
            return None

    def get_elements_text(self, xpath, timeout=300):
        """Wait for multiple elements to load and return their texts."""
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath))
            )
            return [element.text for element in elements]
        except Exception as e:
            print(f"Error getting texts from elements: {xpath}. Exception: {e}")
            return []
