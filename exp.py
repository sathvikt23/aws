import requests
from bs4 import BeautifulSoup

url = "https://www.accuweather.com/en/in/hyderabad/202190/current-weather/202190"  # replace with actual URL
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Use the full selector
element = soup.select_one(
    "body > div > div.two-column-page-content > div.page-column-1 > div.page-content.content-module > div.current-weather-card.card-module.content-module > div.card-content > div.current-weather-extra.no-realfeel-phrase > div"
)

if element:
    print(element.text.strip())
else:
    print("Element not found")
