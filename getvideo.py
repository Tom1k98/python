import requests
from bs4 import BeautifulSoup
from subprocess import PIPE, run
import re
import os
import sys
import time
from mymail import *
import concurrent.futures
import unidecode

TARGET = 'C:/Users/Tomas/Videos'

channels = ['https://www.youtube.com/channel/UCwmiCqC-56bUIdWBd9hTu2g',
'https://www.youtube.com/user/AlexandrasGirlyTalk/videos',
'https://www.youtube.com/user/orionvanessa/videos',
'https://www.youtube.com/channel/UCPQ-f1KEJi-a49SLgYHifUA/videos',
'https://www.youtube.com/channel/UCOPcvkL6SK9GJV4rrWfQ_fQ/videos',
'https://www.youtube.com/user/missAlexandraC/videos',
'https://www.youtube.com/user/BeautyBySiena/videos']

newvid = []

def out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout

def getvid(url):
    site = url
    chan = requests.get(site).text
    soup = BeautifulSoup(chan, 'lxml')
    div = soup.find('div', {'class': 'yt-lockup-content'})
    nazevt = div.h3.a['title']
    linkt = div.h3.a['href']
    nazev = re.sub('[[?!|\*]', '', unidecode.unidecode(nazevt)).replace(' ', '_').replace('&', 'and')
    print('nazev: {}'.format(nazevt))
    print(f'odkaz: https://www.youtube.com{linkt}')
    link = f'https://www.youtube.com{linkt}'
    if os.path.isfile('{}/{}'.format(TARGET, nazev)):
        print('Skipping, already downloaded')
    else:
        print(f"Downloading {nazev}")
        out(f'youtube-dl -f \"bestvideo[ext=mp4],bestaudio\" {link} -o {TARGET}/{nazev}')
        newvid.append(f"nazev: {nazevt}\n")


def sendinfo(to):
    videos = ''.join(newvid)
    message = f'vyslo nove video:\n{videos}'
    subject = 'nova videa'
    mysendmail(to, subject, message)



if __name__ == "__main__":
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(getvid, channels)

    finish = time.perf_counter()
    print(f"Finished in {round(finish-start, 2)} second(s)")
    #sendinfo('petriciecavojova@seznam.cz')