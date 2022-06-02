import sys

import requests
from bs4 import  BeautifulSoup
import os
import json
import threading
def do_request(url):
    try:
        # import ipdb;ipdb.set_trace()
        r1 = requests.get(url)
        return r1
    except Exception as e:
        return 'error'
def do(url):
    r1 = 'error'
    while r1 == 'error':
        r1 = do_request(url)
    return r1

def download_img(url,fullname):
    r1 = do(url)
    f = open(f'{fullname}/{i}.jpg', 'wb')
    f.write(r1.content)
    f.close()

def load_img(fullname,urllist):

    if os.path.exists(fullname):
        print(f'fillname {fullname} has exist')
        return
    else:
        os.mkdir(fullname)

    for i in range(len(urllist)):
        c1=threading.Thread(target=download_img,args=(url,fullname))
        c1.start()
        c1.join()


def check():
    return os.path.realpath(__file__).replace('7mm_home.py','')
    #

basefile=check()

json_7mm = {}
def g2(i,temp):
    r1 = do(temp)
    r2 = BeautifulSoup(r1.text, 'html.parser')
    data = r2.find_all('li', class_="posts-message")
    imgdata=[]
    try:
        imgdata = r2.find_all('div', class_="video-introduction-images-list-row")[0].find_all('img')
    except Exception as e:
        pass
    imglist = []
    for l in imgdata:
        imglist.append(l['src'])
    'class_="video-introduction-images-list-row"'
    name = data[0].text
    time = data[1].text
    long = data[2].text
    id = temp[39:44]

    base = os.path.join(basefile, '7mm_graph', 'jpg', id)
    json_7mm[id] = {
        'name': name,
        'time': time,
        'long': long,
        'url': temp,
        'img': base,
        'imglist': imglist
    }
    print(json_7mm[id])
def g(url):
    r1 = do(url)
    r2 = BeautifulSoup(r1.text, 'html.parser')
    r3 = r2.find_all('img', class_="img-cover")
    r4 = r2.find_all('a', target="_top")
    imglist = []
    detailurlist = []
    temp = []

    for i in r3:
        imglist.append(i['src'])
    for i in r4:
        detailurlist.append(i['href'])
    for i in detailurlist:
        if i.startswith('https://7mmtv.tv/zh/uncensored_content/'):

            temp.append(i)

    temp = list(set(temp))

    for i in range(len(temp)):
        c1 = threading.Thread(target=g2, args=(i,temp[i]))
        c1.start()
        c1.join()



for j in range(1,3):
    url=f'https://7mmtv.tv/zh/uncensored_makersr/37/FC2/{j}.html'

    c1=threading.Thread(target=g,args=(url,))
    c1.start()
    # c1.join()
base2 = os.path.join(basefile,'7mm_graph','index.json')
f2=open(base2,'w')
json.dump(json_7mm,f2)
f2.close()



'''

Traceback (most recent call last):
  File "/Users/storm.shen/web/izone/download/7mm_home.py", line 30, in <module>
    f.write(r1.content)
TypeError: write() argument must be str, not bytes
'''