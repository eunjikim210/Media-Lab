import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL
# Change the URL accordingly in springfieldspringfield
url = 'https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=chicago-p-d-2014'

try:
    # Send an HTTP request to the URL
    response = requests.get(url)
    response.raise_for_status()
    
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all 'a' tags that match the class 'season-episode-title text-dark'
    episodes = soup.find_all('a', class_='season-episode-title text-dark')
    
    titles = []
    links = []
    
    for episode in episodes:
        titles.append(episode.text.strip())
        # Get full links
        links.append('https://www.springfieldspringfield.co.uk/' + episode['href']) 
    
    df = pd.DataFrame({
        'title': titles,
        'link': links
    })
    
    # Change the file name accordingly
    df.to_excel('chicagopd_episodes.xlsx', index=False)

except requests.RequestException as e:
    print(f"An error occurred while requesting the webpage: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
