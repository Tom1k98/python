import requests
from bs4 import BeautifulSoup
from subprocess import PIPE, run


def out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout


def myvid(url):
    site = url
    chan = requests.get(site).text
    soup = BeautifulSoup(chan, 'lxml')
    div = soup.find('div', {'class': 'yt-lockup-content'})
    nazevt = div.h3.a['title']
    linkt = div.h3.a['href']
    print('nazev: {}'.format(nazevt))
    print('odkaz: https://www.youtube.com/{}'.format(linkt))
    link = 'https://www.youtube.com{}'.format(linkt)
    out('youtube-dl {} -o /home/tom/Videos/nvm'.format(link))

def main():
    myvid('https://www.youtube.com/channel/UCwmiCqC-56bUIdWBd9hTu2g')

if __name__ == "__main__":
    main()
