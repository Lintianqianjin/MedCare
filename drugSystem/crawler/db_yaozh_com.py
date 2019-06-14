import requests
from lxml import etree

preurl = 'https://db.yaozh.com/unlabeleduse?'
page = 1
sufurl = '&pageSize=20'

url = f'{preurl}{page}{sufurl}'

def mainCrawl(url):
    sess = requests.session()
    sess.get(url)
    print(f'{url}')