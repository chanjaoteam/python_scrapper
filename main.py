from input_handler import prompt_for_url
from session_manager import SessionManager
from product_listing import ProductListing
from product_detail import ProductDetail
from rate_limiter import RateLimiter
from logger import setup_logger

def main():
    setup_logger()
    url = prompt_for_url()
    
    session_manager = SessionManager()
    session_manager.attach_or_launch()
    
    product_listing = ProductListing(session_manager.driver)
    product_listing.scrape_listings(url)
    
    product_detail = ProductDetail(session_manager.driver)
    product_detail.scrape_details()
    
    session_manager.close_session()

if __name__ == "__main__":
    main()
