import asyncio
import aiohttp
import time
from aiomultiprocess import Pool

start = time.time()

async def get(url):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    result = await response.text()
    #在close前加上await否则显示close is not awaited
    await session.close()
    return result

async def request():
    url = 'http://127.0.0.1:5000'
    urls = [url for _ in range(100)]
    async with Pool() as pool:
        result = await pool.map(get, urls)
        return result

if __name__=='__main__':
    ##要加name main这句，不然会报错在windows系统上
    coroutine = request()
    task = asyncio.ensure_future(coroutine)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)

    end = time.time()
    print('Cost time:', end - start)