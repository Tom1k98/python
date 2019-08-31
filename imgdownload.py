#!/usr/bin/env python3
import requests
import shutil

def downloadimg(url, namet):
    tmp = url.split(".")
    atta = tmp[-1]
    name = '{}.{}'.format(namet, atta)
    path = '/home/tom/Pictures/{}'.format(name)
    r = requests.get(url)
    with open(path, 'wb') as f:
        f.write(r.content)

def prompt():
    site = input("zadej url obrazku: ")
    nazev = input("zadej nazev souboru: ")

def main():
