import requests
from bs4 import BeautifulSoup
import re
import csv
import sys
import time

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
            komentar = getcommnets(odkaz)
            with open(FILE, 'a') as file:
                if isWritten():
                    updateComments(komentar)
                else:
                    csvw = csv.writer(file)
                    csvw.writerow([datum, nazev, odkaz, komentar])
                    #print(f"{odkaz} - {datum} - {nazev}")
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

def updateComments(commn):
 
    if commn != getcommnets(odkaz):
        commn = getcommnets(odkaz)
        text = 'comment update'
        file = open(FILE, 'a')
        csvw = csv.writer(file)
        csvw.writerow([datum, nazev, odkaz, commn, text])
       # print("comment updated")
    else:
        pass
        #  print('no update')
    #print(f"{odkaz} - {datum} - {nazev}")



def isWritten():
    with open(FILE) as file:
        lines = file.readlines()
        for line in lines:
            if nazev in line:
                return True


if __name__ == "__main__":
        while 1>0:
            getnews()
            time.sleep(600)
            


