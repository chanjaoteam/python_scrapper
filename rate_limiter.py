import random
import time

class RateLimiter:
    def __init__(self, min_delay=5, max_delay=20):
        self.min_delay = min_delay
        self.max_delay = max_delay

    def wait(self):
        """Introduce a random delay between requests."""
        delay = random.randint(self.min_delay, self.max_delay)
        print(f"Waiting for {delay} seconds...")
        time.sleep(delay)
