# import os
#
# file='/Users/storm.shen/web/qa/视频'
#
# for root, dirs, files in os.walk(file):
#
#         # root 表示当前正在访问的文件夹路径
#         # dirs 表示该文件夹下的子目录名list
#         # files 表示该文件夹下的文件list
#
#         # 遍历文件
#         for f in files:
#             if f.endswith('Chinese homemade video.m3u8'):
#                 f2=open('视频/'+f,'r')
#                 print(f)
#                 fname=open('clear/'+str(f).replace('.m3u8','.mp4'),'ab')
#                 f3=f2.readlines()
#                 for i in range(len(f3)):
#                     f3[i]=f3[i].replace('storage/emulated/0/QQBrowser','/Users/storm.shen/web/qa')
#                 for i in f3:
#                     if i.startswith('file://'):
#                         f4=open(i.replace('file:///','').replace('\n',''),'rb')
#
#                         print(f4)
#                         import ipdb;ipdb.set_trace()
#                         #
#                         # fname.write(f4.read())
#
#             # print(os.path.join(root, f))
#         #
#         # # 遍历所有的文件夹
#         # for d in dirs:
#         #     print(os.path.join(root, d))
#
import requests
from bs4 import BeautifulSoup
import os
import  cloudscraper
cloud = cloudscraper.create_scraper()


def get_ts(id,headers,name):
    i=0
    url=f'https://la.killcovid2021.com/m3u8/{id}/{id}{i}.ts'
    fname = file.join(name)
    print(fname)
    r1='error'
    while r1=='error':
        r1=do_request(url)
        # import ipdb;ipdb.set_trace()

    temp1=int(r1.status_code)
    import ipdb;ipdb.set_trace()
    os.mkdir(fname)

    while(temp1==200):

        url = f'https://la.killcovid2021.com/m3u8/{id}/{id}{i}.ts'
        print(f'{name}     {url}    {temp1}')

        temp1 = int(r1.status_code)
        video = open(f'{fname}/{i}.ts', 'ab')
        video.write(r1.content)
        video.close()
        r1 = 'error'
        while r1 == 'error':
            r1 = do_request(url)

        i+=1
url=[]
video=[]
user_agent ='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
headers = { 'User-Agent' : user_agent,
            'Referer': 'https://91porn.com/',
'sec-ch-ua-platform': "macOS",
'cookie':'CLIPSHARE=h9c6dpp4gfk0lj72c14nictnuk',
'Connection':'keep-alive',
'accept-language': 'zh-CN,zh'
            }

numbers=[]
video_info={}
have_down=[]
def get_have_down():
    f=open('have_downloaded.txt','r')
    f1=f.readline()
    while (f1):
        have_down.append(f1[0:6])
        f1 = f.readline()
    f.close()
print(get_have_down())
def do_request(url):
    try:
        # import ipdb;ipdb.set_trace()
        r1 = cloud.get(url, headers=headers)
        return r1
    except Exception as e:
        print(str(e))
        return 'error'

def pa(url3):
    t=[]
    for i in range(1,1000):
        try:
            admit=1
            uname=url3+f'&page={i}'
            r1 = 'error'
            while r1 == 'error':
                r1 = do_request(uname)
            r1=r1.text
            f2 = BeautifulSoup(r1, 'html.parser')
            temp=f2.find_all('source')
            foname=f2.find('h4', class_="login_register_header").text.find('Public')
            author=f2.find('h4', class_="login_register_header").text[0:foname].replace(' ','')
            name=[i.text for i in f2.find_all('span',class_="video-title")]#video name

            if name==t:
                break
            else:
                t=name
            f3=f2.find_all('div',class_="col-xs-12 col-sm-4 col-md-3 col-lg-3")
            j=0

            for k in f3:
                url2=k.find('a')['href']
                print(url2)
                # import ipdb;ipdb.set_trace()
                r1 = 'error'
                while r1 == 'error':
                    r1 = do_request(url2)
                r1 = r1.text
                f2=BeautifulSoup(r1, 'html.parser')
                time=f2.find_all('span',class_="video-info-span")[0].text+' '
                temp = f2.find_all(style="display:none;")[1].text#ts id
                video_info[name[j]]={
                    'author':author,
                    'url':url2,
                    'ts':temp,
                }
                print(temp+'  '+time+name[j])
                if temp in have_down:
                    j = j + 1
                    continue
                get_ts(temp,headers,time+name[j])
                f6=open('have_downloaded.txt','a')
                f7=open('have_downloaded_info.txt','a')
                f6.writelines(temp+'  '+name[j]+'\n')
                have_down.append(temp)
                f6.close()

                j=j+1
        except Exception as e:
            print(str(e))

            continue



file= os.path.dirname(os.path.abspath(__file__))+'/video'
file2=os.path.dirname(os.path.abspath(__file__))+'/归档'
file3=os.path.dirname(os.path.abspath(__file__))+'/归档4'
file4=os.path.dirname(os.path.abspath(__file__))+'/have_downloaded.txt'
os.path.exists(file)
def m3u82mp4(ts,name):

    ts.sort(key=lambda x:int(x.replace('.ts','')))
    ts.pop()
    f=open(f'{file3}/{name}.mp4','ab')
    for s in ts:
        try:
            f2=open(f'{file}/{name}/{s}','rb')
            # print(f'/归档/{file}/{name}/{s}')
            f.write(f2.read())
        except Exception as e:
            print(str(e))
            continue
    f.close()

def turn():
    exist_video = []
    for root, dirs, files in os.walk(file2):
        if dirs:
            c = dirs

        # 遍历文件
        for f in files:
            if f.endswith('.mp4'):
                exist_video.append(f.replace('.mp4', ''))

    i=0

    for root, dirs, files in os.walk(file):

            # root 表示当前正在访问的文件夹路径
            # dirs 表示该文件夹下的子目录名list
            # files 表示该文件夹下的文件list
            # c=[]
            # c.append('')
            if dirs:
                c1=[]
                c1=dirs
                c1.insert(0,' ')
            # import ipdb;ipdb.set_trace()
            ts=[]

            # 遍历文件

            for f in files:

                if f.endswith('.ts'):
                    ts.append(f)
            # import ipdb;ipdb.set_trace()
            # if ts:
            #     print('pass')
            #     continue
            # else:
            #     print(ts)
            if ts and c1[i] not in exist_video :
                print('转换 '+c1[i])
                m3u82mp4(ts,c1[i])
                i+=1
            else:
                print('不转换 ',c1[i])
                i += 1
            if i==len(c1):
                break


view=[]
video1=[]
def get_info():
    f=open('1111.txt')
    for i in f.readlines():
        if len(i)<10:
            continue
        print(i.split()[0][19:20]) #u为单个  v为主页
        print(i.split()[0][19:20]=='v')
        if i.split()[0][19:20]=='v':
            view.append(i.split()[0])
        elif i.split()[0][19:20]=='u':
            video1.append(i.split()[0])
    return view,video1
def check():
    check_file_exist(file)
    check_file_exist(file3)
    check_file_exist(file4)
def check_file_exist(file):
    if not os.path.exists(file):
        os.mkdir(file)
check()
get_info()

for i in video1:
    pa(i)

# turn()
import ipdb;ipdb.set_trace()


