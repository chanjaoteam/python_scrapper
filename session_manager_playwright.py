import psutil
import asyncio
from playwright.async_api import async_playwright

class SessionManagerPW:
    def __init__(self, debug_port=9222):
        self.debug_port = debug_port
        self.browser = None
        self.page = None

    async def attach_or_launch(self):
        """Attach to an existing Chrome session or launch a new one with debugging enabled."""
        # Check if there's an existing Chrome session with remote debugging
        chrome_processes = [
            p for p in psutil.process_iter(attrs=['pid', 'name', 'cmdline'])
            if p.info['name'] == 'chrome.exe'
        ]

        print("Checking for existing Chrome sessions...")

        if chrome_processes:
            for proc in chrome_processes:
                print("Process found: ", proc.info)
                if '--remote-debugging-port=9222' in proc.info['cmdline']:
                    print("Attaching to existing Chrome session...")
                    await self.connect_to_browser()
                    return

        print("No active Chrome session found. Launching a new Chrome session with debugging enabled.")
        await self.launch_new_chrome()

    async def connect_to_browser(self):
        """Connects to an existing Chrome session using the debugging protocol."""
        async with async_playwright() as playwright:
            # Connect to the existing Chrome session
            self.browser = await playwright.chromium.connect_over_cdp(f'http://localhost:{self.debug_port}')
            self.page = await self.browser.new_page()
            print("Successfully attached to the existing Chrome session.")

    async def launch_new_chrome(self):
        """Launches a new Chrome session with remote debugging enabled."""
        async with async_playwright() as playwright:
            # Launch a new Chromium browser instance with remote debugging
            self.browser = await playwright.chromium.launch(headless=False, args=[f'--remote-debugging-port={self.debug_port}'])
            self.page = await self.browser.new_page()
            print("New Chrome session launched with debugging enabled.")

    async def close_session(self):
        """Close the Chrome session."""
        if self.browser:
            await self.browser.close()
            print("Chrome session closed.")

    def run(self):
        """Run the session manager asynchronously."""
        asyncio.run(self.attach_or_launch())
