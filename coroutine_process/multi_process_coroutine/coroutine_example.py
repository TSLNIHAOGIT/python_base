import asyncio
import aiohttp
import time
import numpy

start = time.time()
import numpy as np
async def get(url):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    result = await response.text()
    await session.close()
    # result = np.dot(np.random.random((7000, 1000)), np.random.random((1000, 7000)))

    return result

async def request():
    url = 'http://127.0.0.1:5000'
    print('Waiting for', url)
    result = await get(url)
    print('Get response from', url, 'Result:', result)
    return  result

tasks = [asyncio.ensure_future(request()) for _ in range(500)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

##运行结束后返回结果在task中
for each in tasks:
    print('fff',each.result())

end = time.time()
print('Cost time:', end - start)