import os
import json
import sys
import threading
import copy
import requests
import shutil

def download_img(url,fullname,i):
    r1 = do(url)
    f = open(f'{fullname}/{i}.jpg', 'wb')
    print(f'{fullname}/{i}.jpg')
    f.write(r1.content)
    f.close()
def check():
    return os.path.realpath(__file__).replace('dir.py','')
    #
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
basefile=check()
f=open('all.json','r')
f1 = json.load(f)
c2=[]
i1=0
def down_mkdir(f1):
    for k,v in f1.items():
        fullname = os.path.join(basefile, '7mm_graph', 'jpg', k)
        if os.path.exists(fullname):
            print(f'{k} has exist')
            continue
        else:
            os.mkdir(fullname)
        for i in range(len(v['imglist'])):
            c1=threading.Thread(target=download_img,args=(v['imglist'][i],fullname,i,))
            c1.start()
            c2.append(c1)

    for i in c2:
        i.join()


def big(f1):#统计所有图片大小
    sum=0
    for k,v in f1.items():
        sum+=len(v['imglist'])
    print(sum*100/1024/1024)
data1={}
data2={}
def count():#统计每个文件夹图片数量

    file1=os.path.join(basefile,'7mm_graph','jpg')
    print(file1)
    f3=[]
    f4=[]
    f3=os.listdir(file1)
    if '.DS_Store' in f3:
        f3.remove('.DS_Store')

    # for f1,f2,ff3 in os.walk(file1):
    #     f3=copy.deepcopy(f2)
    #     break

    for i in f3:
        file2=os.path.join(file1,i)
        data1[i] = len(os.listdir(file2))
    return data1
print(count())

def should():#每个文件夹应有个数
    for k,v in f1.items():
        data2[k]=len(v['imglist'])
    return data2
should()
unfinish={}
dell=[]
for k,v in data2.items():
    if v==data1.get(k):
        pass
    else:
        if data1.get(k) :
            file1 = os.path.join(basefile, '7mm_graph', 'jpg',k)
            dell.append(file1)
            print(v,data1.get(k))
        unfinish[k]=f1.get(k)
# for i in unfinish:
#     print(i)
print(len(unfinish))
print(dell)
for i in dell:
    shutil.rmtree(i)
# down_mkdir(unfinish)



