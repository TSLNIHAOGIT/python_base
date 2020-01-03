import asyncio
import aiohttp
import time
from aiomultiprocess import Pool
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor,wait,as_completed

start = time.time()

async def get(url):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    result = await response.text()
    #在close前加上await否则显示close is not awaited
    await session.close()
    return result
async def get_future(future):
    # res=await future
    res=future
    return res

async def request():

    url = 'http://127.0.0.1:5000'
    urls = [url for _ in range(10)]

    max_workers=5
    it_ls = []
    with futures.ProcessPoolExecutor(max_workers) as executor:
        for url in urls:
            print('start url',url)
            future = executor.submit(get, url)
            it_ls.append(future)
        # # 如果采用FIRST_COMPLETED参数，程序并不会等到线程池里面所有的任务都完成。
        # finished_future,unfinished_future=wait(it_ls, return_when='FIRST_COMPLETED')
    all_completed_res=[]
    for i, future in enumerate(as_completed(it_ls, timeout=2400)):
            result=await get_future(future)
            all_completed_res.append(result)
    return all_completed_res

    # async with Pool() as pool:
    #     #结果是一个list
    #     result = await pool.map(get, urls)
    #     print('Get response from', url, 'Result:', result)
    #     return result

if __name__=='__main__':
    ##要加name main这句，不然会报错在windows系统上
    coroutine = request()
    task = asyncio.ensure_future(coroutine)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)

    end = time.time()
    print('Cost time:', end - start)