import pandas as pd
import os 
from datetime import datetime

tmp = datetime.now()
timestamp = tmp.strftime("%m%Y")
check = tmp.strftime("%d")
IN_FILE = 'novinky.csv'
OUT_FILE = f'csv/novinky-{timestamp}.csv'
def rmduplicate():
    if os.path.exists(OUT_FILE) or check < '30':
        pass
    else:
        df = pd.read_csv(IN_FILE, sep=',', encoding='utf-8')
        df.columns = ['datum', 'titulek', 'odkaz', 'komentare', 'text', 'rubrika']
        df.drop_duplicates(subset='titulek',inplace = True, keep = 'last')
        df.to_csv(OUT_FILE, encoding='utf-8')
