import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.livemint.com/mutual-fund/page-600'
livement_url = 'https://www.livemint.com'

mutual_fund = "https://www.livemint.com/mutual-fund"

count = 0

status = 200
while(status ==200):
    
    mutual_fund_page = mutual_fund + "page-" + str(count)
    page = requests.get(url)
    status = page.status_code
    count+=1
    print(count)
    print("length of links")
    
    

# Send request to the page
page = requests.get(url)
print(page)
# Check if request is successful
if page.status_code == 200:
    print("Page fetched successfully")
else:
    print(f"Failed to fetch page. Status code: {page.status_code}")
    exit()

# Parse HTML content with BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')

# Find links to articles
links = []
for a in soup.find_all('h2', {'class': 'headline'}):
    for i in a.find_all('a', href=True):
        link = i['href']
        # Make sure the link is a full URL
        full_url = livement_url + link if link.startswith('/') else link
        links.append(full_url)

# Initialize lists to store article data
title = []
date = []
s_date = []
text = []
print("length of links")
print(len(links))
# Loop through each article link
for l in links:
    try:
        fetch = requests.get(l)
        if fetch.status_code == 200:
            sp = BeautifulSoup(fetch.content, 'html.parser')
            print(l)
            
		
            # Extract title
            # x = sp.find("h1", { "class" : "headline" }).text.strip()
            # title.append(x)
            
            # Extract publication date
            # y = sp.find("span", { "class" : "articleInfo pubtime" }).text.strip()
            # date.append(y)
            
            # # Extract text content
            # z = sp.find("div", { "class" : "mainArea" }).text.strip()
            # text.append(z)
        else:
            print(f"Failed to fetch article {l}. Status code: {fetch.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching article {l}: {e}")

# Create a DataFrame with the data
df2 = pd.DataFrame(list(zip(title, links, date, text)), 
                   columns=['title', 'link', 'publish_date', 'text'])

# Save DataFrame to CSV
df2.to_csv('livemint.csv', index=False)

print("Scraping complete and data saved to 'livemint.csv'.")
