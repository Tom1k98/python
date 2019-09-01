import requests
from bs4 import BeautifulSoup
from subprocess import PIPE, run
import re
import os
import sys
import smtplib
import psutil
import base64


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
    text = msg.as_string() # You now need to convert the MIMEMultipart object to a string to send
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
        sys.exit()
    else:
        out('youtube-dl {} -o ~/Videos/{}'.format(link, nazev))
        zprava = "vyslo nove video s nazvem {}".format(nazevt)
        sendmail('patriciecavojova@seznam.cz', zprava)



def main():
    getvid('https://www.youtube.com/channel/UCwmiCqC-56bUIdWBd9hTu2g')

if __name__ == "__main__":
    main()
