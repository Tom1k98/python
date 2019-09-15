import requests
from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime
import sys

SITE = 'https://www.novinky.cz/stalo-se'
FILE = '/home/tom/novinky.csv'
datum = 'a'
nazev = 'a'
tmp = datetime.now()
timestamp = tmp.strftime("%d%m%Y%H%M%S")

def getnews():
    url = requests.get(SITE).text
    tmp = BeautifulSoup(url, 'lxml')
    for scrp in tmp.findAll('div', {'class': 'f_bB'}):
        try:
            datum = re.sub('[^0-9:]', '', scrp.text)[:5]
            nazev = scrp.h3.text.replace(':', '')
            print(f"{nazev} - {datum}")
        except:
            pass

def writecsv():
    with open(FILE, 'a') as file:
        csvw = csv.writer(file)
        csvw.writerow([timestamp, datum, nazev])
    file.close()

def check():
    with open(FILE) as file:
        line = file.readlines()
        if timestamp in line:
            print('today records already written')
            sys.exit()


if __name__ == "__main__":
    getnews()
    check()
    writecsv()