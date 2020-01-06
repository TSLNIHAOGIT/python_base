# 线程池：
from concurrent.futures import ThreadPoolExecutor
from concurrent import futures
import urllib.request
import time


from concurrent.futures import ThreadPoolExecutor,wait,as_completed
import urllib.request
import numpy as np
import asyncio
import threading
import multiprocessing
from multiprocessing import Queue ,Pool,Process
#import aiohttp
import os


# URLS = ['https://github.com/','http://www.163.com', 'https://www.baidu.com/' ]
# #执行单个任务，即只下载一个链接
# async def load_url(url):
#     np.power(np.random.rand(), 2)
#     print('start url',url)
#     with urllib.request.urlopen(url, timeout=60) as conn:
#         print('end %r page is %d bytes' % (url, len(conn.read())))
#
# def process_go(*namelist):
#     tasks=[]
#     loop=asyncio.get_event_loop()
#     for name in namelist:
#         tasks.append(asyncio.ensure_future(hello(name)))
#     loop.run_until_complete(asyncio.wait(tasks))
#
#
# executor = ThreadPoolExecutor(max_workers=3)
#
# f_list = []
# for url in URLS:
#     '''asyncio.ensure_future('''
#     # future = executor.submit(load_url,url)
#     future = executor.submit(load_url, url)
#     f_list.append(future)
# # 如果采用默认的ALL_COMPLETED，程序会阻塞直到线程池里面的所有任务都完成，再执行主线程：
# #如果采用FIRST_COMPLETED参数，程序并不会等到线程池里面所有的任务都完成。
# print(wait(f_list,return_when='FIRST_COMPLETED'))
#
# print('主线程')




import asyncio
import threading
import multiprocessing
from multiprocessing import Queue ,Pool,Process
#import aiohttp
import os

#定义协程coroutine
async def hello(name):
    print('hello {}{}**********{}'.format(name,os.getpid(),threading.current_thread()))
    #await asyncio.sleep(int(name))
    #协程遇到await，事件循环将会挂起该协程，执行别的协程，直到其他的协程也挂起或者执行完毕，再进行下一个协程的执行
    await asyncio.sleep(1)
    print('end:{}{}'.format(name,os.getpid()))

def process_start(*namelist):
    tasks=[]
    #创建事件循环
    loop=asyncio.get_event_loop()
    for name in namelist:
        #通过loop.create_task(coroutine)创建task,同样的可以通过 asyncio.ensure_future(coroutine)创建task
        tasks.append(asyncio.ensure_future(hello(name)))

    # 将任务加入到事件循环loop
    #此时我们使用了aysncio实现了并发。asyncio.wait(tasks)，接受一个task列表
    # 也可以使用 asyncio.gather(*tasks) ,接收一堆task
    loop.run_until_complete(asyncio.wait(tasks))

def task_start(namelist):
    i=0
    lst=[]
    flag=10
    while namelist:
        '''
        动态的构造任务数，创建进程：
        此处是10个数字为一组任务，创建一个进程，该进程去控制协程对象然后执行一组任务
        '''
        i+=1
        l=namelist.pop()
        lst.append(l)
        if i==flag:
            p=Process(target=process_start,args=lst)
            p.start()
            #p.join()
            lst=[]
            i=0
    if namelist!=[]:
        p=Process(target=process_start,args=lst)
        p.start()
        #p.join()
if __name__=='__main__':
    start=time.time()
    namelist=list('0123456789'*10)
    task_start(namelist)
    print('耗时',time.time()-start)
'''
loop=asyncio.get_event_loop()
tasks=[]
namelist=list('0123456789'*10)
for i in namelist:
    tasks.append(asyncio.ensure_future(hello(i)))
loop.run_until_complete(asyncio.wait(tasks))'''
