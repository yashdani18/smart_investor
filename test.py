import requests
from bs4 import BeautifulSoup

# url = 'https://www.screener.in/company/GPIL/consolidated/'
url = 'https://www.screener.in/company/NSLNISP/consolidated'
response = requests.get(url)
print(response.status_code)
