from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DynamicContentHandler:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, xpath, timeout=10):
        """Wait for a specific element to load on the page."""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
