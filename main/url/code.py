import requests
from bs4 import BeautifulSoup

def scrape_nse_beml_announcements():
    """
    Scrapes the NSE India BEML announcements table inside the div with id 'corpAnnouncementTable'
    """
    url = "https://www.nseindia.com/get-quotes/equity?symbol=BEML#Announcements"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.nseindia.com/',
    }

    try:
        session = requests.Session()
        session.headers.update(headers)

        response = session.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # ✅ Step 1: Find the outer div
        main_div = soup.find('div', class_='main')
        if not main_div:
            raise Exception("Main div not found")

        # ✅ Step 2: Go deeper into nested structure and find the announcement table div
        announcement_div = main_div.find('div', id='corpAnnouncementTable')
        if not announcement_div:
            raise Exception("Announcement div with id='corpAnnouncementTable' not found")


        print(announcement_div.prettify())  # For debugging, to see the structure
        # ✅ Step 3: Find the table
        table = announcement_div.find('table')
        if not table:
            raise Exception("Table not found inside the announcement div")

        # ✅ Step 4: Extract rows from the table body
        tbody = table.find('tbody')
        rows = tbody.find_all('tr') if tbody else []

        announcements = []
        for row in rows:
            columns = row.find_all('td')
            row_data = [col.get_text(strip=True) for col in columns]
            announcements.append(row_data)

        # ✅ Output to file
        with open("announcements.txt", "w", encoding="utf-8") as file:
            for row in announcements:
                file.write("\t".join(row) + "\n")

        print(f"✅ Extracted {len(announcements)} announcement rows. Saved to announcements.txt")

        return announcements

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("NSE India BEML Announcements Scraper")
    print("=" * 50)
    scrape_nse_beml_announcements()
