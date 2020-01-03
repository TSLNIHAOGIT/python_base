# 线程池：
from concurrent.futures import ThreadPoolExecutor
from concurrent import futures
import urllib.request
# URLS = ['https://github.com/','http://www.163.com', 'https://www.baidu.com/']
# def load_url(url):
#     with urllib.request.urlopen(url, timeout=60) as conn:
#         print('%r page is %d bytes' % (url, len(conn.read())))
#
# executor = ThreadPoolExecutor(max_workers=3)
#
# for url in URLS:
#     future = executor.submit(load_url,url)
#     print(future.done())
#
# print('主线程')

# # 运行结果：
# False
# False
# False
# 主线程
# 'https://www.baidu.com/' page is 227 bytes
# 'http://www.163.com' page is 662047 bytes
# 'https://github.com/' page is 54629 bytes
# 进程池：同上
# from concurrent.futures import ProcessPoolExecutor
# import urllib.request
# URLS = ['https://github.com/','http://www.163.com', 'https://www.baidu.com/', ]
# def load_url(url):
#     with urllib.request.urlopen(url, timeout=60) as conn:
#         print('%r page is %d bytes' % (url, len(conn.read())))
#         return url
#
# executor = ProcessPoolExecutor(max_workers=3)
# if __name__ == '__main__': # 要加main
#     it_ls = []
#     for url in URLS:
#         #submit按照完成的先后顺序返回
#         future = executor.submit(load_url,url)
#         print(future.done())
#         it_ls.append(future)
#     ##as_completed加不加线程中的任务都是异步提交，但是，如果加了as_completed必须等到线程中的任务都完成了，才会进行下面的操作
#     #如输出主线程;否则整个过程都是异步的，可以先输出主线程在现实那些url,类似wait中的all_completed
#     done_iter = futures.as_completed(it_ls)  # as_completed()返回迭代器
#     print(done_iter)
#     for x in done_iter:  # x是future对象
#         print('res', x.result())
#     print('主线程')


from concurrent.futures import ThreadPoolExecutor,wait,as_completed
import urllib.request
import numpy as np
import asyncio
import threading
import multiprocessing
from multiprocessing import Queue ,Pool,Process
#import aiohttp
import os
async def hello(name):
    print('hello {}{}**********{}'.format(name,os.getpid(),threading.current_thread()))
    #await asyncio.sleep(int(name))
    await asyncio.sleep(1)
    print('end:{}{}'.format(name,os.getpid()))
def process_start(*namelist):
    tasks=[]
    loop=asyncio.get_event_loop()
    for name in namelist:
        tasks.append(asyncio.ensure_future(hello(name)))
    loop.run_until_complete(asyncio.wait(tasks))


URLS = ['https://github.com/','http://www.163.com', 'https://www.baidu.com/' ]
def load_url(url):
    np.power(np.random.rand(), 2)
    print('start url',url)
    with urllib.request.urlopen(url, timeout=60) as conn:
        print('end %r page is %d bytes' % (url, len(conn.read())))

executor = ThreadPoolExecutor(max_workers=3)

f_list = []
for url in URLS:
    '''asyncio.ensure_future('''
    # future = executor.submit(load_url,url)
    future = executor.submit(load_url, url)
    f_list.append(future)
# 如果采用默认的ALL_COMPLETED，程序会阻塞直到线程池里面的所有任务都完成，再执行主线程：
#如果采用FIRST_COMPLETED参数，程序并不会等到线程池里面所有的任务都完成。
print(wait(f_list,return_when='FIRST_COMPLETED'))

print('主线程')

# # 运行结果：
# 'http://www.163.com' page is 662047 bytes
# 'https://www.baidu.com/' page is 227 bytes
# 'https://github.com/' page is 54629 bytes
# DoneAndNotDoneFutures(done={<Future at 0x2d0f898 state=finished returned NoneType>, <Future at 0x2bd0630 state=finished returned NoneType>, <Future at 0x2d27470 state=finished returned NoneType>}, not_done=set())
# 主线程

# #运行结果：
# False  #　子进程只完成创建，并没有执行完成
# False　
# False
# 主线程　＃　子进程创建完成就会向下执行主线程，并不会等待子进程执行完毕
# 'http://www.163.com' page is 662049 bytes
# 'https://www.baidu.com/' page is 227 bytes
# 'https://github.com/' page is 54629 bytes

#
# from concurrent.futures import ThreadPoolExecutor
# import urllib.request
# URLS = ['https://github.com/','http://www.163.com', 'https://www.baidu.com/', ]
# def load_url(url):
#     print('start',url)
#     with urllib.request.urlopen(url, timeout=60) as conn:
#         print('end %r page is %d bytes' % (url, len(conn.read())))
#
# executor = ThreadPoolExecutor(max_workers=3)
#
# executor.map(load_url,URLS)
#
# print('主线程')
# #
# # # 运行结果：
# # 主线程
# # 'http://www.163.com' page is 662047 bytes
# # 'https://www.baidu.com/' page is 227 bytes
# # 'https://github.com/' page is 54629 bytes