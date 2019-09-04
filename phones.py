import requests
from bs4 import BeautifulSoup
import re

nazev = []
cena = []
link = []

def collect():
    url = requests.get('https://www.alza.cz/nejprodavanejsi-nejlepsi-mobily/18843445.htm').text
    data = BeautifulSoup(url, 'lxml')
    for top in data.find_all('a', {'class': 'name browsinglink'}):
        final = top.text
        nazev.append(final)
        link.append(f"alza.cz{top['href']}")
    for price in data.find_all('span', {'class': 'c2'}):
        final2 = price.text
        cenan = re.sub('[^0-9]+', '', final2)
        cena.append(cenan)

def vypis():
    place = 1
    celkem = zip(nazev, cena, link)
    for naz, cen, lin in celkem:
        print(f"{place}: {naz} - {cen},-\nlink: {lin}")
        print()
        place += 1

if __name__ == "__main__":
    collect()
    vypis()
