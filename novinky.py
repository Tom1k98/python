import requests
from bs4 import BeautifulSoup
import csv
import sys
import time
import re
from datetime import datetime

SITE = 'https://www.novinky.cz/stalo-se'
FILE = '/home/tom/novinky.csv'
datum = ''
nazev = ''
odkaz = ''
komentar = ''


def getnews():
    global datum
    global nazev
    global odkaz
    global komentar
    url = requests.get(SITE).text
    tmp = BeautifulSoup(url, 'lxml')
    for scrp in tmp.findAll('div', {'class': 'f_bz'}):
        try:
            nazev = scrp.h3.text.replace(':', '')
            odkaz = scrp.a['href']
            komentar = getcommnets(odkaz)
            with open(FILE, 'a') as file:
                if isWritten():
                    if updateComments():
                        text = "update comment"
                        csvw = csv.writer(file)
                        csvw.writerow([cas, nazev, odkaz, komentar, text])
                    else:
                        pass
                else:
                    text = "new article"
                    csvw = csv.writer(file)
                    csvw.writerow([cas, nazev, odkaz, komentar, text])
            file.close()
        except:
            pass

def getcommnets(od):
    try:
        url = requests.get(od).text
        tmp = BeautifulSoup(url, 'lxml')
        comm = tmp.find('span', {'class': 'q_fX'})
        comm = re.sub('[^0-9]', '', comm.text)
        return comm
    except:
        pass

def getCategory():
    url = requests.get('https://www.novinky.cz/domaci/clanek/znojmo-slavilo-vinobrani-dorazily-tisice-lidi-40296544').text
    tmp = BeautifulSoup(url, 'lxml')
    for category in tmp.find('div', {'class': ''}):
        print(category)

def updateComments():
    with open(FILE) as file_n:
        lines = file_n.readlines()
        for line in lines:
            if komentar in line:
                return False
            else:
                pass
    return True

def isWritten():
    with open(FILE) as file:
        lines = file.readlines()
        for line in lines:
            if nazev in line:
                return True


if __name__ == "__main__":
    tmp = datetime.now()
    cas = tmp.strftime("%d.%m.%Y %H:%M")
    getnews()
    #getCategory()
            


