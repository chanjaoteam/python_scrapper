import psutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class SessionManager:
    def __init__(self, debug_port=8989):
        self.debug_port = debug_port
        self.driver = None

    def attach_or_launch(self):
        """Attach to an existing Chrome session or launch a new one with debugging enabled."""
        # Check if there's an existing Chrome session with remote debugging

        chrome_names = []

        

        chrome_processes = [
            p for p in psutil.process_iter(attrs=['pid', 'name', 'cmdline']) 
            if p.info['name'] == 'chrome.exe' and '--remote-debugging-port=8989' in p.info['cmdline']
        ]
        print("is chrome exists")

        print(chrome_names)
        print(bool(chrome_processes))
        
        if chrome_processes:
            print("Attaching to existing Chrome session...")
            options = webdriver.ChromeOptions()
            options.add_experimental_option("debuggerAddress","localhost:8989")
            # options.debugger_address = f"localhost:{self.debug_port}"
            try:
                self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                # self.driver = webdriver.Chrome(executable_path="C:\\Users\\user\\Documents\\Projects\\webscrapper_prompt_pj\\scrapper_code",chrome_options=options)
                print("Successfully attached to the existing Chrome session.")
            except Exception as e:
                print(f"Failed to attach: {e}. Launching a new Chrome session instead.")
                self.launch_new_chrome()
        else:
            print("No active Chrome session found. Launching a new Chrome session with remote debugging enabled.")
            self.launch_new_chrome()

    def launch_new_chrome(self):
        """Launches a new Chrome session with remote debugging enabled."""
        options = webdriver.ChromeOptions()
        options.add_argument(f"--remote-debugging-port={self.debug_port}")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print("New Chrome session launched with debugging enabled.")

    def close_session(self):
        """Close the Chrome session."""
        if self.driver:
            self.driver.quit()
            print("Chrome session closed.")
