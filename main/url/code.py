import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def scrape_nse_beml_basic():
    """
    Basic scraping approach using requests and BeautifulSoup
    """
    url = "https://www.nseindia.com/get-quotes/equity?symbol=BEML"
    
    # Headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        # Create a session to maintain cookies
        session = requests.Session()
        session.headers.update(headers)
        
        # First, get the main page to establish session
        response = session.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for div with class "setting wrap data"
        target_div = soup.find('div', class_='main')
        
        if target_div:
            print("Found div with class 'main':")
            print("-" * 50)
            print(target_div.prettify())
            return target_div
        else:
            print("Div with class 'main' not found")
            # Let's also check for similar classes
            print("\nSearching for similar classes...")
            divs_with_setting = soup.find_all('div', class_=lambda x: x and 'setting wrap' in x)

            
            print(f"Found {len(divs_with_setting)} divs with 'setting wrap' in class")

            
            return None
            
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

if __name__ == "__main__":
    print("NSE India BEML Data Scraper")
    print("=" * 50)
    
    print("\n1. Trying basic scraping approach...")
    basic_result = scrape_nse_beml_basic()
    
    
    print("\n3. Trying Selenium approach...")
    print("Note: This requires ChromeDriver to be installed")
    print("Install with: pip install selenium")
    print("Download ChromeDriver from: https://chromedriver.chromium.org/")
    
    # Uncomment the line below if you have Selenium and ChromeDriver set up
    # selenium_result = scrape_nse_beml_selenium()
    
    print("\nScraping complete!")