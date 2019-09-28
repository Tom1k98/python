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
import sqlite3

channels = ['https://www.youtube.com/channel/UCwmiCqC-56bUIdWBd9hTu2g',
'https://www.youtube.com/user/AlexandrasGirlyTalk/videos',
'https://www.youtube.com/user/orionvanessa/videos',
'https://www.youtube.com/channel/UCPQ-f1KEJi-a49SLgYHifUA/videos',
'https://www.youtube.com/channel/UCOPcvkL6SK9GJV4rrWfQ_fQ/videos',
'https://www.youtube.com/user/missAlexandraC/videos',
'https://www.youtube.com/user/BeautyBySiena/videos']

newvid = []
linktovid = []

def getvid(url):
    site = url
    chan = requests.get(site).text
    soup = BeautifulSoup(chan, 'lxml')
    div = soup.find('div', {'class': 'yt-lockup-content'})
    nazevt = div.h3.a['title']
    linkt = div.h3.a['href']
    nazev = re.sub('[[?!|\*]', '', unidecode.unidecode(nazevt)).replace(' ', '_').replace('&', 'and')
    link = f'https://www.youtube.com{linkt}'
    lframe_tmp = linkt.split('=')[1]
    link_frame = f'https://www.youtube.com/embed/{lframe_tmp}'
    if isVideo(nazev):
        print('Skipping, already added')
    else:
        print(f"Adding {nazevt}")
        addVideo(nazev)
        newvid.append(f"nazev: {nazevt}\n")
        linktovid.append(f"<iframe width=\"420\" height=\"315\" src={link_frame}></iframe>")


def sendinfo(to):
    videos = ''.join(newvid)
    message = f'vyslo nove video:\n{videos}'
    subject = 'nova videa'
    mysendmail(to, subject, message)

def makeHtml():
    start_html = '<html><head></head><body>'
    frames_tmp = ''.join(linktovid)
    end_html = '</body></html>'
    frames = f'{start_html} {frames_tmp} {end_html}'
    with open('index.html', 'w') as html_file:
        html_file.write(frames)

def addVideo(vid):
    conn = sqlite3.connect('videos.db')
    c = conn.cursor()
    add = """
    INSERT INTO videos (nazev) VALUES (?)
    """
    c.execute(add, (vid, ))
    conn.commit()
    conn.close()

def isVideo(vid):
    conn = sqlite3.connect('videos.db')
    c = conn.cursor()
    sql = """
    SELECT * FROM videos WHERE nazev=?
    """
    c.execute(sql, (vid,))
    return True if len(c.fetchall())>0 else False

def makeTable():
    conn = sqlite3.connect('videos.db')
    c = conn.cursor()
    table = """
    CREATE TABLE IF NOT EXISTS videos (
        id integer PRIMARY KEY AUTOINCREMENT,
        nazev text
    )
    """
    c.execute(table)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    makeTable()
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(getvid, channels)

    finish = time.perf_counter()
    print(f"Finished in {round(finish-start, 2)} second(s)")
    sendinfo('tomas.storc@gmail.com')
    makeHtml()