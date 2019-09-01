#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

tmp = datetime.now()
date = tmp.strftime("%d.%m.%Y")
weat = requests.get('https://pocasi.seznam.cz/praha?lat=50.0848&lon=14.4112&z=5&f=muni').text
data = BeautifulSoup(weat, 'lxml')
final = data.find('button', {'class': 'd_gQ'})
dnestt = final.div.text
dnest = re.sub('[^0-9/]+', '', dnestt).split('/')
max = dnest[0]
min = dnest[1]
print('maximalni teplota dnes {} bude {}, nejnizsi denni teplota bude {}'.format(date, max, min))
