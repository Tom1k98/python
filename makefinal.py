import pandas as pd

IN_FILE = 'novinky.csv'
OUT_FILE = 'final.csv'

df = pd.read_csv(IN_FILE, sep=',', encoding='utf-8')
df.columns = ['datum', 'titulek', 'odkaz', 'komentare', 'text', 'rubrika']

df.drop_duplicates(subset='titulek',inplace = True, keep = 'last')
df.to_csv(OUT_FILE, encoding='utf-8')
