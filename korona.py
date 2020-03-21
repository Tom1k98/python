#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import lxml
from datetime import datetime

OUT_FILE = '/Users/tom/Library/Mobile Documents/com~apple~Numbers/Documents/cases.csv'

url = requests.get('https://onemocneni-aktualne.mzcr.cz/covid-19')
soup = BeautifulSoup(url.text, 'lxml')

now = datetime.now()
time = now.strftime("%d.%m.%Y %H:%M")

def casesNum():
    getNumC = soup.find('p', {'id': 'count-sick'})
    return getNumC.text

def recoverNum():
    getNumR = soup.find('p', {'id': 'count-recover'})
    return getNumR.text

def testsNum():
    getNumT = soup.find('p', {'id': 'count-test'})
    return getNumT.text

def writeToFile():
    with open(OUT_FILE, 'a+') as file:
        file.write(f'{time},{testsNum()},{casesNum()},{recoverNum()}\n')

def checkUpdate():
    latestf = soup.find('p', {'id': 'count-sick'}).text
    with open(OUT_FILE) as file:
        lines = file.readlines()
        for line in lines:
            if str(latestf) in line:
                return True
        return False

if __name__ == "__main__":
    #print(f'{time} - {testsNum()} - {casesNum()} - {recoverNum()}')
    writeToFile() if checkUpdate() else print('nezapsano')