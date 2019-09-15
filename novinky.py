import requests
from bs4 import BeautifulSoup
import re
import csv
import sys

SITE = 'https://www.novinky.cz/stalo-se'
FILE = '/home/tom/novinky.csv'
datum = ''
nazev = ''
odkaz = ''


def getnews():
    global datum
    global nazev
    global odkaz
    url = requests.get(SITE).text
    tmp = BeautifulSoup(url, 'lxml')
    for scrp in tmp.findAll('div', {'class': 'f_bz'}):
        try:
            datum = re.sub('[^0-9:]', '', scrp.text)[:5]
            nazev = scrp.h3.text.replace(':', '')
            odkaz = scrp.a['href']
            with open(FILE, 'a') as file:
                if isWritten():
                    print("already written")
                else:
                    csvw = csv.writer(file)
                    csvw.writerow([datum, nazev, odkaz])
                    #print(f"{odkaz} - {datum} - {nazev}")
            file.close()
        except:
            pass


def isWritten():
    with open(FILE) as file:
        lines = file.readlines()
        for line in lines:
            if nazev in line:
                return True

            pass

if __name__ == "__main__":
    getnews()

