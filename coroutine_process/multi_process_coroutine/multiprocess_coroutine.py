import asyncio
import aiohttp
import time
from aiomultiprocess import Pool
from coroutine_process.multi_process_coroutine.arcfour import arcfour

JOBS = 12
SIZE = 2**18

KEY = b"'Twas brillig, and the slithy toves\nDid gyre"
STATUS = '{} workers, elapsed time: {:.2f}s'
from random import randrange
async def arcfour_test(size, key=KEY):
    in_text = bytearray(randrange(256) for i in range(size))
    cypher_text = arcfour(key, in_text)
    out_text = arcfour(key, cypher_text)
    assert in_text == out_text, 'Failed arcfour_test'
    return size
start = time.time()
import numpy as np
async def compute_dot():
    print('go compute')
    res=np.dot(np.random.random((7000, 1000)), np.random.random((1000, 7000)))
    print('res',res)
    return res
async def get(url):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    result = await response.text()
    # result_temp=await compute_dot()
    # result=str(result)+str(result_temp)
    #在close前加上await否则显示close is not awaited
    await session.close()
    return result

async def request():
    url = 'http://127.0.0.1:5000'
    urls = [url for _ in range(100)]
    all_size=[]
    for i in range(JOBS, 0, -1):
        size = SIZE + int(SIZE / JOBS * (i - JOBS / 2))
        all_size.append(size)
    async with Pool(3) as pool:
        # result = await pool.map(get, urls)

        result = await pool.map(arcfour_test, all_size)
        print('res',result)
        return result

if __name__=='__main__':
    ##要加name main这句，不然会报错在windows系统上
    coroutine = request()
    task = asyncio.ensure_future(coroutine)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)

    print('coroutine',coroutine)
    print('task',task.result())
    # for each in coroutine:
    #     print('res111',each)

    end = time.time()
    print('Cost time:', end - start)#Cost time: 194.59068775177002
