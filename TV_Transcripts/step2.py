import pandas as pd
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

# Change the file name accordingly
df = pd.read_excel('chicagopd_episodes.xlsx')

wb = Workbook()
ws = wb.active
ws.title = "Episodes Content"

ws.append(["Title", "Link", "Script Content"])

for index, row in df.iterrows():
    try:
        link = row['link']
        title = row['title']
        
        # Send an HTTP request to get the page content
        response = requests.get(link)
        # Ensure the request was successful
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        script_container = soup.find('div', class_='scrolling-script-container')
        
        # Clean the text: remove <br> tags and excess whitespace
        script_text = script_container.get_text(separator=' ', strip=True)
        
        ws.append([title, link, script_text])
        
    except Exception as e:
        print(f"Error processing {link}: {e}")
        ws.append([title, link, "Error retrieving or processing script"])

# Change the file name accordingly
wb.save("chicagopd_episodes_cleaned.xlsx")
