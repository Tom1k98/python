import requests
from bs4 import BeautifulSoup
import argparse
import re

nazev = []
cena = []
link = []
heureka = []

def collect():
    url = requests.get('https://www.alza.cz/nejprodavanejsi-nejlepsi-mobily/18843445.htm').text
    data = BeautifulSoup(url, 'lxml')
    for top in data.find_all('a', {'class': 'name browsinglink'}):
        final = top.text
        forheureka = final.replace(' ', '+')
        nazev.append(final)
        link.append(f"alza.cz{top['href']}")
        heureka.append(forheureka)
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

def porovnej():
    index = 0
    for phone in heureka:
        try:
            url = requests.get(f'https://www.heureka.cz/?h%5Bfraze%5D={phone}').text
            data = BeautifulSoup(url, 'lxml')
            cenaheu = data.find('a', {'class': 'pricen'})
            print(f"{nazev[index]}:\n\theureka - {cenaheu.text}\n\talza - {cena[index]}")
            index += 1
        except:
            print("")
            print(f"Nenalezena zadna data pro: {phone.replace('+', ' ')}")
            print("")
            pass

if __name__ == "__main__":
    collect()
    vypis()
    porovnej()
