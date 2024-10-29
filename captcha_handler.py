class CaptchaHandler:
    def __init__(self):
        pass

    def detect_captcha(self, driver):
        """Detect CAPTCHA prompts on the page."""
        try:
            captcha_element = driver.find_element("xpath", "//div[contains(@class, 'captcha')]")
            return captcha_element.is_displayed()
        except Exception:
            return False

    def handle_captcha(self):
        """Notify the user to resolve CAPTCHA manually."""
        print("CAPTCHA detected. Please resolve it manually and press Enter to continue...")
        input()
