#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import sys
import csv

tmp = datetime.now()
date = tmp.strftime("%d.%m.%Y")

def check():
    with open('/home/tom/data/pocasi.csv') as file:
        line = file.read()
        if date in line:
            print('today records already written')
            sys.exit()


def getvalues():
    weat = requests.get('https://pocasi.seznam.cz/praha?lat=50.0848&lon=14.4112&z=5&f=muni').text
    data = BeautifulSoup(weat, 'lxml')
    final = data.find('button', {'class': 'd_gQ'})
    dnes = final.div.text
    dnes = re.sub('[^0-9/]+', '', dnes).split('/')
    max = dnes[0]
    min = dnes[1]
    print('maximalni teplota dnes {} bude {}, nejnizsi denni teplota bude {}'.format(date, max, min))

    with open('/home/tom/data/pocasi.csv', 'a') as csv_file:
        csv_w = csv.writer(csv_file)
        csv_w.writerow([date, max, min])
    csv_file.close()


def main():
    check()
    getvalues()

if __name__ == '__main__':
    main()
