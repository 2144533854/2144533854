import random
import time
from queue import Empty

import PySimpleGUI as sg
import threading
import queue
from contextlib import closing
from requests import get
# 布局，是一个用户定义的二维列表。
# 第一维德元素分居不同的行上,第二维度上的元素们居于同一行,不同列上
# 此处定义的列表  由三部分组成 Text文件 ProgressBar进度条 Cancel取消按钮构成

# 队列 后进先出
q = queue.Queue()
q1 = queue.Queue()
headers={ 'Content-Type': 'text/html'}
proxies={'http':None,'https':None}
def mian2(url,q):
    try :
        # response.headers['content-length']得到的数据类型是str而不是int
        content_size = random.randint(1000000,2000000)
        data_count = 0  # 当前已传输的大小
        size=int(content_size / 1024 )
        print(f' is downloading....  size: {size}mb')

        while(data_count<=content_size):
            # done_block = int((data_count / content_size) * 50)
            # 已经下载的文件大小
            data_count = data_count + 40000
            time.sleep(0.3)
            # 实时进度条进度

            now_jd = (data_count / content_size) * 100
            print(f'now_jd  {now_jd}   data_count {data_count}    content_size  {content_size}')
            q.put(now_jd )  # 向队列中放入当前任务完成度
            print('finish')
        return '2'
    except Exception as e:
        # print(e)
        return 'error'


def mian(url,q):
    try :
        with closing(get(url, stream=True,headers=headers)) as response:
            print(response.headers)
            name = url[len(url) - 18:]
            chunk_size = 4096  # 单次请求最大值
            # response.headers['content-length']得到的数据类型是str而不是int
            content_size = int(response.headers['content-length'])  # 文件总大小
            data_count = 0  # 当前已传输的大小
            size=int(content_size / 1024 / 1024)
            # print(f'{name} is downloading....  size: {size}mb')
            with open(f'{size}mb+{name}', "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    done_block = int((data_count / content_size) * 50)
                    # 已经下载的文件大小
                    data_count = data_count + len(data)
                    # 实时进度条进度
                    now_jd = (data_count / content_size) * 100
                    q.put({'name':name,'size':size,'data_count':data_count / 1024 / 1024,'now_jd':now_jd})  # 向队列中放入当前任务完成度
            print(name+'finish')
                    # %% 表示%

            return '2'
    except Exception as e:
        print(e)
        return 'error'






def main2(url,q):
    er='error'
    while(er=='error'):
        er=mian(url,q)
def task_1(q):
    for i in range(50):
        # 因为要大于window.read设置超时时间100ms 保证读取时队列最多只有一个元素
        time.sleep(random.uniform(0,1.5))
        q.put(i + 1)  # 向队列中放入当前任务完成度

# 创建多线程 设置以保护模式启动，即主线程运行结束，子线程也停止运行
tasklist=[]
queuelist=[]
barlist=[]
urllist=['https://sto056.akamai-cdn-content.com/tysxeywbos66j6cdaa5rbrcaox6jijgwgapimmuxvq375m26e2dkpmjj3wlq/FC2PPV-2295651.mp4',
         'https://sto088.akamai-cdn-content.com/tysxf5xgp666j6cdabtbbviaggscvl66dskdb45ggw5xxjuuoflpvuxuamga/FC2PPV-2245120.mp4',
         'https://sto027.akamai-cdn-content.com/tysxerttp666j6cdabxrbgcufftgyoc7urray3zft66bnercnowhdpsgs2tq/FC2PPV-2242100.mp4']
layout = [[sg.Text('任务完成进度')],
          [sg.Cancel()]]
n=3
for i in range(n):

    layout.append([sg.Text('',key=f'name{i}'),sg.ProgressBar(50, orientation='h', size=(50, 20), key=f'progressbar{i}'),sg.Text('',key=f'data_count{i}'),sg.Text('',key=f'size{i}'),sg.Text('',key=f'now_jd{i}')])
    queuelist.append(queue.Queue())
# window只需将自定义的布局加载出来即可 第一个参数是窗口标题。
window = sg.Window('机器人执行进度', layout)

# 根据key值获取到进度条


for i in range(n):
    barlist.append(window[f'progressbar{i}'])
    print(urllist[i],queuelist[i])
    worker_task = threading.Thread(target=main2,args=(urllist[i],queuelist[i],))
    worker_task.setDaemon(True)
    worker_task.start()


while True:  # 死循环不断读取队列中数据，直到读到100
    # event 就是返回的事件
    # 如点击Cancel后    event=Cancel
    event, values = window.read(timeout=100)
    if event == 'Cancel' or event is None:
        # 点击取消按钮或者返回事件为 None
        break
    valuelist = []
    # 10ms 无操作算超时event会等于 __TIMEOUT__
    # 其实不用判断
    try:
        # get是等待读取，直到读取到数据
        #  get_nowait 不等待，读取不到数据 就报异常
        for i in range(n):
            t=queuelist[i].get_nowait()
            valuelist.append(t)
            # print(f'-------------bar{i} value is {t}')


    except Empty:  # 没有读取到数据的话，继续window.read
        continue
    else:  # 读取到数据
        for i in range(n):
            print(f'bar{i} value is {valuelist[i]}')
            name=valuelist[i].get('name')

            size=valuelist[i].get('size')
            data_count=valuelist[i].get('data_count')
            print(data_count)
            now_jd=valuelist[i].get('now_jd')
            barlist[i].UpdateBar(now_jd)
            if name:
                window[f'name{i}'].update(name)
            if size:
                window[f'size{i}'].update(str(size)+'mb')
            if data_count>=0 and data_count is not None:
                print(data_count)
                print(window[f'data_count{i}'].update(str(round(data_count,3))+'mb/'))
            if now_jd:
                window[f'now_jd{i}'].update(str(round(int(now_jd*100),3))+'%')

        # if valuelist[i] == 50:  # 进度满跳出循环
        #     break
def mian(url,q):
    try :
        with closing(get(url, stream=True)) as response:
            name = url[len(url) - 18:]
            chunk_size = 4096  # 单次请求最大值
            # response.headers['content-length']得到的数据类型是str而不是int
            content_size = int(response.headers['content-length'])  # 文件总大小
            data_count = 0  # 当前已传输的大小
            size=int(content_size / 1024 / 1024)
            # print(f'{name} is downloading....  size: {size}mb')
            with open(f'{size}mb+{name}', "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    done_block = int((data_count / content_size) * 50)
                    # 已经下载的文件大小
                    data_count = data_count + len(data)
                    # 实时进度条进度
                    now_jd = (data_count / content_size) * 100
                    q.put({'name':name,'size':size,'data_count':data_count / 1024 / 1024,'now_jd':now_jd})  # 向队列中放入当前任务完成度
            print(name+'finish')
                    # %% 表示%

            return '2'
    except Exception as e:
        # print(e)
        return 'error'

def mian2(url,q):
    try :
        # response.headers['content-length']得到的数据类型是str而不是int
        content_size = random.randint(1000000,2000000)
        data_count = 0  # 当前已传输的大小
        size=int(content_size / 1024 )
        # print(f' is downloading....  size: {size}mb')

        while(data_count<=content_size):
            # done_block = int((data_count / content_size) * 50)
            # 已经下载的文件大小
            data_count = data_count + 40000
            time.sleep(0.3)
            # 实时进度条进度

            now_jd = (data_count / content_size) * 100
            print(f'now_jd  {now_jd}   data_count {data_count}    content_size  {content_size}')
            q.put(now_jd )  # 向队列中放入当前任务完成度
            print('finish')
        return '2'
    except Exception as e:
        # print(e)
        return 'error'

window.close()