import requests
from bs4 import BeautifulSoup
import csv
import sys
import time
import re
from datetime import datetime
import makefinal as mf

SITE = 'https://www.novinky.cz/stalo-se'
FILE = '/home/tom/novinky.csv'
datum = ''
nazev = ''
odkaz = ''
komentar = ''
kategorie = ''
category = []

def getnews():
    global datum
    global nazev
    global odkaz
    global komentar
    global kategorie
    url = requests.get(SITE).text
    tmp = BeautifulSoup(url, 'lxml')
    for scrp in tmp.findAll('div', {'class': 'f_bz'}):
        try:
            nazev = scrp.h3.text.replace(':', '')
            odkaz = scrp.a['href']
            komentar = getcommnets(odkaz)
            kategorie = getCategory(odkaz)
            with open(FILE, 'a') as file:
                if isWritten():
                    if updateComments():
                        text = "update comment"
                        csvw = csv.writer(file)
                        csvw.writerow([cas, nazev, odkaz, komentar, text, kategorie])
                    else:
                        pass
                else:
                    text = "new article"
                    csvw = csv.writer(file)
                    csvw.writerow([cas, nazev, odkaz, komentar, text, kategorie])
            file.close()
        except:
            pass

def getcommnets(od):
    try:
        url = requests.get(od).text
        tmp = BeautifulSoup(url, 'lxml')
        comm = tmp.find('span', {'class': 'q_ga'})
        comm = re.sub('[^0-9]', '', comm.text)
        return comm
    except:
        pass

def getCategory(kat):
    global category
    category = []
    url = requests.get(kat).text
    tmp = BeautifulSoup(url, 'lxml')
    for items in tmp.find('div', {'class': 'f_au'}):
        cat_final = items.text
        category.append(cat_final)
    return category[1]
    

def updateComments():
    with open(FILE) as file_n:
        lines = file_n.readlines()
        for line in lines:
            if nazev in line:
                if komentar in line:
                    return False
        return True

def isWritten():
    with open(FILE) as file:
        lines = file.readlines()
        for line in lines:
            if nazev in line:
                return True

def getCommentsAll():
    with open(FILE) as file_n:
        lines = file_n.readlines()
        for line in lines:
            with open(FILE, 'a') as file:
                tmp = line.split(".")
                url = tmp[2]
                kom_update = getcommnets(url)
                csv_update = csv.writer(file)
                csv_update.writerow([tmp[0], tmp[1], tmp[2], kom_update,])




if __name__ == "__main__":
    tmp = datetime.now()
    cas = tmp.strftime("%d.%m.%Y %H:%M")
    getnews()
    mf.rmduplicate()
  
            


