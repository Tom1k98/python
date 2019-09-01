import requests
from bs4 import BeautifulSoup
from subprocess import PIPE, run
import re
import os
import sys
import smtplib
import psutil
import base64

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

def sendmail(to, text):

    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    email = 'tomas.storc@afd.cz'
    password = 'Youmb609.'
    send_to_email = to
    subject = 'nove video' # The subject line
    message = text

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('mail.afd.cz', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()


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
        #out('youtube-dl {} -o ~/Videos/{}'.format(link, nazev))
        newvid.append("nazev: {}\n".format(nazevt))


def sendinfo(to):
    videos = ''.join(newvid)
    message = f'vyslo nove video:\n{videos}'
    sendmail(to, message)



def main():
    for i in channels:
        getvid(i)

    sendinfo('patriciecavojova@seznam.cz')

if __name__ == "__main__":
    main()
