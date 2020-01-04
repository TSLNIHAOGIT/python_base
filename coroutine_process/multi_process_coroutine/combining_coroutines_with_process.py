import asyncio
import concurrent.futures
import logging
import sys
import time
import asyncio
import aiohttp
import time
from aiomultiprocess import Pool
import requests



async def get(url):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    result = await response.text()
    #在close前加上await否则显示close is not awaited
    await session.close()
    return result
def sub_loop(urls):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [get(url) for url in urls]
    results = loop.run_until_complete(asyncio.gather(*tasks))

    ##这是所有的任务已经完成了
    print('res000',results)
    # for num, result in results:
    #     print('fetch({}) = {}'.format(num, result))
    return results


async def run(executor, urls=None):
    log = logging.getLogger('run_blocking_tasks')
    log.info('starting')
    log.info('creating executor tasks')
    loop = asyncio.get_event_loop()
    url = 'http://127.0.0.1:5000'
    urls = [url for _ in range(500)]
    results=await loop.run_in_executor(executor, sub_loop,urls)
    # await asyncio.get_event_loop().run_in_executor(executor, sub_loop,urls)
    # results = [t.result() for t in completed]
    log.info('results: {!r}'.format(results))
    #
    # log.info('exiting')
def get_url(url):
        return requests.get(url)
# async def request():
#     url = 'http://127.0.0.1:5000'
#     urls = [url for _ in range(10)]
#     async with Pool() as pool:
#         result = await pool.map(get, urls)
#         return result

async def run_blocking_tasks_request(executor):
    log = logging.getLogger('run_blocking_tasks')
    log.info('starting')

    log.info('creating executor tasks')
    loop = asyncio.get_event_loop()
    url = 'http://127.0.0.1:5000'
    urls = [url for _ in range(5)]

    blocking_tasks = [
        # 一个进程去控制多个协程
        loop.run_in_executor(executor, get_url, url)
        # loop.run_in_executor(executor, get, url)

        for url in urls
    ]
    log.info('waiting for executor tasks')
    completed, pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    log.info('results: {!r}'.format(results))

    log.info('exiting')


def blocks(n):
    log = logging.getLogger('blocks({})'.format(n))
    log.info('running')
    time.sleep(6)
    # asyncio.sleep(6)#这个是在协程上使用的，模拟IO操作，让出控制权，在此处没有意义
    log.info('done')
    return n ** 2


async def run_blocking_tasks(executor):
    log = logging.getLogger('run_blocking_tasks')
    log.info('starting')

    log.info('creating executor tasks')
    loop = asyncio.get_event_loop()
    blocking_tasks = [
        loop.run_in_executor(executor, blocks, i)
        for i in range(10)
    ]
    log.info('waiting for executor tasks')
    completed, pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    log.info('results: {!r}'.format(results))

    log.info('exiting')


# if __name__ == '__main__':
#     # Configure logging to show the name of the thread
#     # where the log message originates.
#     logging.basicConfig(
#         level=logging.INFO,
#         format='%(threadName)10s %(name)18s: %(message)s',
#         stream=sys.stderr,
#     )
#
#     # Create a limited thread pool.
#     executor = concurrent.futures.ThreadPoolExecutor(
#         max_workers=3,
#     )
#
#     # Create a limited process pool.
#     # executor = concurrent.futures.ProcessPoolExecutor(
#     #         max_workers=3,
#     #     )
#
#     event_loop = asyncio.get_event_loop()
#     try:
#         event_loop.run_until_complete(
#             run_blocking_tasks(executor)
#         )
#     finally:
#         event_loop.close()

if __name__ == '__main__':
    start=time.time()
    # Configure logging to show the id of the process
    # where the log message originates.
    logging.basicConfig(
        level=logging.INFO,
        format='PID %(process)5s %(name)18s: %(message)s',
        stream=sys.stderr,
    )

    # Create a limited process pool.
    executor = concurrent.futures.ProcessPoolExecutor(
        max_workers=4,
    )

    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(
            # run_blocking_tasks(executor)
            # run_blocking_tasks_request(executor)
            run(executor)
        )
    finally:
        event_loop.close()
    print(time.time()-start)#100个url,10进程耗时32s

'''
这个程序虽然能运行但是逻辑上不是我想要的，因为这里开一个进程时，就是按照顺序进行的，并没有异步的进行
（可能是time.sleep造成的，也就是我的调用方法错误造成的么）；
但是多个进程确实进行了并行处理
###这里的逻辑估计是多个进程，每个进程独立并行的运行并控制多个协程


'''
