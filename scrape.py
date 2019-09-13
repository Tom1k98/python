#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import re
import sys


compoment = {'update': 'sec_dpkg', 
             'qmail': 'qmail_stat'}

bigmac = ['http://a1-bigmacl2-1.ko.seznam.cz:8000/', 'http://a1-bigmacl2-2.ko.seznam.cz:8000/', 'http://a1-bigmacl2-1.ng.seznam.cz:8000/', 'http://a1-bigmacl2-1.ng.seznam.cz:8000/']

def select():
    global service
    selected = sys.argv[1]
    service = compoment.get(selected)
    print(service)

def getdata(webpage):
    url = requests.get(webpage).text
    plainhtml = str(BeautifulSoup(url, 'lxml'))
    with open('html', 'w+') as file:
        file.write(plainhtml)
        file.close()
    with open('html', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if 'bigmac_check' in line:
                pass
            else:
                if service in line and 'wallet' not in line:
                    tmp = line.split(',')
                    host = tmp[4]
                    host = re.sub("[\"=]", "", host).replace("host", "")
                    loc = tmp[10]
                    if 'kokura' in loc:
                        print(f"{host}.ko.seznam.cz", end=" " )
                    elif 'nagano' in loc:
                        print(f"{host}.ng.seznam.cz", end=" ")
                    else:
                        print('')

        file.close()

def scrapuj():
    print(f"vybrany servery pro: {service}")
    for wp in bigmac:
        getdata(wp)
    print(" ")

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("je nutno vybrat skupinu serveru")
        print("..................")
        print("dostupne skupiny:\n\tupdate - servery kde je potreba udelat secure updaty\n\tqmail - servery kde pravdepodobne nebezi szn-qmaill")
        sys.exit()

    select()
    scrapuj()
