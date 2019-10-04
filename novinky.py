import requests
from bs4 import BeautifulSoup
import csv
import sys
import time
import re
from datetime import datetime, date
import os
import pandas as pd

line = datetime.now()
cas = line.strftime("%d.%m.%Y %H:%M")
month = line.strftime("%m")
day = line.strftime("%d")

SITE = 'https://www.novinky.cz/stalo-se'
FILE = '/home/tom/novinky.csv'
OUT_FILE = f'/home/tom/csv/endofmonth/novinky-{month}.csv'
COMM_FILE = f'/home/tom/csv/novinky_comments_{month}.csv'

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
    line = BeautifulSoup(url, 'lxml')
    for scrp in line.findAll('div', {'class': 'f_bz'}):
        try:
            nazev = re.sub('[:,]', '', scrp.h3.text)
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
        line = BeautifulSoup(url, 'lxml')
        comm = line.find('span', {'class': 'q_gg'})
        comm = re.sub('[^0-9]', '', comm.text)
        return comm
    except:
        pass

def getCategory(kat):
    global category
    category = []
    url = requests.get(kat).text
    line = BeautifulSoup(url, 'lxml')
    for items in line.find('div', {'class': 'f_au'}):
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

def rmduplicate():
        df = pd.read_csv(FILE, sep=',', encoding='utf-8')
        df.columns = ['datum', 'titulek', 'odkaz', 'komentare', 'text', 'rubrika']
        df.drop_duplicates(subset='titulek',inplace = True, keep = 'last')
        df.to_csv(OUT_FILE, encoding='utf-8')

def getCommentsAll():
    with open(OUT_FILE) as file_n:
        lines = csv.reader(file_n, delimiter=',')
        for line in lines:
                print(line)
                kom_update = getcommnets(line[3])
                with open(COMM_FILE, 'a') as file:
                    csv_update = csv.writer(file)
                    csv_update.writerow([line[1], line[2], line[3], kom_update, line[5], line[6]])


if __name__ == "__main__":
    getnews()
    if day == '1':
        if os.path.isfile(COMM_FILE):
            sys.exit()
        else:
            rmduplicate()
            getCommentsAll()
        
    
  
            


