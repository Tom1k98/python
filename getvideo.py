import requests
from bs4 import BeautifulSoup
from subprocess import PIPE, run
import re
import os
import sys
import time
from mymail import *
import concurrent.futures


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
    nazev = re.sub('[^A-Za-z0-9]+', '', nazevt)
    print('nazev: {}'.format(nazevt))
    print('odkaz: https://www.youtube.com/{}'.format(linkt))
    link = 'https://www.youtube.com{}'.format(linkt)
    if os.path.isfile('/home/tom/Videos/{}'.format(nazev)):
        print('soubor je jiz stazen')
    else:
        print(f"Downloading {nazev}")
        out('youtube-dl {} -o ~/Videos/{}'.format(link, nazev))
        newvid.append("nazev: {}\n".format(nazevt))


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
    print(f"Downloaded in {round(finish-start, 2)} second(s)")
    #sendinfo('petriciecavojova@seznam.cz')