import requests
from bs4 import BeautifulSoup
import lxml

url = requests.get('https://onemocneni-aktualne.mzcr.cz/covid-19')
soup = BeautifulSoup(url.text, 'lxml')

def casesNum():
    getNumC = soup.find('p', {'id': 'count-sick'})
    return getNumC.text
def recoverNum():
    getNumR = soup.find('p', {'id': 'count-recover'})
    return getNumR.text
if __name__ == "__main__":
    print(f'{casesNum()} - {recoverNum()}')