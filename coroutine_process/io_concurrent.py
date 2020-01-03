import time
import asyncio
from threading import Thread


async def do_task(params):  # 执行单个任务
    print(time.time(), params)
    await asyncio.sleep(1)  # 注意这里不能用time.sleep()，否则全局都会sleep
    print(time.time(), params)
    return params


async def do_task_group(params_group):  # 执行多个任务
    tasks = [asyncio.ensure_future(do_task(params), loop=io_loop) for params in params_group]
    results = await asyncio.gather(*tasks, loop=io_loop, return_exceptions=True)
    return results


async def do_task_groups(all_params, send_step=5):  # 执行多个任务组
    # 把所有任务按照步长分成多个任务组
    params_groups = [all_params[index: index + send_step] for index in range(0, len(all_params), send_step)]
    tasks = [asyncio.ensure_future(do_task_group(params_group), loop=io_loop) for params_group in params_groups]

    # 获取并合并任务结果
    the_results = await asyncio.gather(*tasks, loop=io_loop, return_exceptions=True)
    results = []
    for result in the_results:
        results.extend(result)
    return results


def do_all_tasks(all_params):  # 执行所有任务
    results = asyncio.run_coroutine_threadsafe(do_task_groups(all_params), io_loop)
    print('Start all task in', time.time())
    return results.result()  # 阻塞式获取结果，真正阻塞执行事务的地方


def start_loop():  # 启动事件循环
    io_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(io_loop)
    thread = Thread(target=io_loop.run_forever)
    thread.daemon = True
    thread.start()
    return io_loop


if __name__ == '__main__':
    io_loop = start_loop()
    all_params = list(range(10))
    print(do_all_tasks(all_params))
