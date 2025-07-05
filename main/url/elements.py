from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Path to your chromedriver
CHROMEDRIVER_PATH = "/path/to/chromedriver"  # ← CHANGE THIS

# Set up Chrome in headless mode
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Hide browser window
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# Create driver
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# Visit the NSE stock quote page for BEML
url = "https://www.nseindia.com/get-quotes/equity?symbol=BEML"
driver.get(url)

# Wait for JavaScript to load content
time.sleep(6)

# Try extracting the div with ID corpAnnouncementTable
try:
    announcement_div = driver.find_element(By.ID, "corpAnnouncementTable")
    print("Corporate Announcements HTML:\n")
    print(announcement_div.get_attribute('outerHTML'))  # You can also use innerHTML
except Exception as e:
    print("Error: Could not find corpAnnouncementTable. Details:", e)

driver.quit()
