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

import asyncio
import time
from concurrent.futures import ProcessPoolExecutor


def cpu_bound_operation(x):
    # time.sleep(x)  # This is some operation that is CPU-bound
    asyncio.sleep(x)
    return x



async def main():
    # Run cpu_bound_operation in the ProcessPoolExecutor
    # This will make your coroutine block, but won't block
    # the event loop; other coroutines can run in meantime.
    # await loop.run_in_executor(p, cpu_bound_operation, 5)

    blocking_tasks = [
        loop.run_in_executor(p, cpu_bound_operation, 2)
        for i in range(6)
    ]

    completed, pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    print('results',results)


# async def run_blocking_tasks(executor):
#     log = logging.getLogger('run_blocking_tasks')
#     log.info('starting')
#
#     log.info('creating executor tasks')
#     loop = asyncio.get_event_loop()
#     blocking_tasks = [
#         loop.run_in_executor(executor, blocks, i)
#         for i in range(6)
#     ]
#     log.info('waiting for executor tasks')
#     completed, pending = await asyncio.wait(blocking_tasks)
#     results = [t.result() for t in completed]
#     log.info('results: {!r}'.format(results))
#
#     log.info('exiting')

if __name__=='__main__':
    start=time.time()
    loop = asyncio.get_event_loop()
    p = ProcessPoolExecutor(1)  # Create a ProcessPool with 2 processes
    loop.run_until_complete(main())
    print('耗时',time.time()-start)