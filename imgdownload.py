#!/usr/bin/env python3
import requests
import shutil

base_path = '/home/tom/Pictures'
def downloadimg(url, namet):
    tmp = url.split(".")
    atta = tmp[-1]
    name = '{}.{}'.format(namet, atta)
    path = '{}/{}'.format(base_path, name)
    r = requests.get(url)
    with open(path, 'wb') as f:
        f.write(r.content)

def prompt():
    site = input("zadej url obrazku: ")
    nazev = input("zadej nazev souboru: ")
    downloadimg(site, nazev)

def main():
    prompt()

if __name__ == "__main__":
    main()
