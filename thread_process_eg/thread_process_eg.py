#!/bin/env python
from multiprocessing import Process
from multiprocessing import freeze_support,Pool
import os
import time
import os

import multiprocessing
import time
# def fork_eg():
#     #linux系统下可用forK函数
#     print( 'Process (%s) start...' % os.getpid())
#     pid = os.fork()
#     if pid==0:
#         print( 'I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
#         os._exit(1)
#     else:
#         print ('I (%s) just created a child process (%s).' % (os.getpid(), pid))

#使用multiprocessing
# def run_proc(name):
#     time.sleep(3)
#     print('Run child process %s (%s)...' % (name, os.getpid()))
# def run_proc_main():
#     print('Parent process %s.' % os.getpid())
#     processes = list()
#     for i in range(5):
#         p = Process(target=run_proc, args=('test',))
#         print('Process will start.')
#         p.start()
#         processes.append(p)
#
#     for p in processes:
#         p.join()
#     print('Process end.')

###使用进程池
#1、使用 multiprocessing.Pool 非阻塞

# def func(msg):
#     print( "msg:", msg)
#     time.sleep(3)
#     print ("end")
# def func_main():
#     pool = multiprocessing.Pool(processes=3)
#     for i in range(3):
#         msg = "hello %d" % (i)
#         pool.apply_async(func, (msg,))
#
#     print("Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~")
#     pool.close()
#     pool.join()  # behind close() or terminate()
#     print( "Sub-process(es) done.")

# if __name__ == '__main__':
    # run_proc_main()
    # func_main()



def Foo(i):
    time.sleep(2)
    print('___time---', time.ctime())
    return i + 100


def Bar(arg):
    print('----exec done:', arg, time.ctime())


if __name__ == '__main__':
    freeze_support()
    pool = Pool(3)  # 线程池中的同时执行的进程数为3

    for i in range(4):
        print('i={}'.format(i))
        pool.apply(func=Foo, args=(i,))

    print('end')
    pool.close()
    pool.join()  # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
