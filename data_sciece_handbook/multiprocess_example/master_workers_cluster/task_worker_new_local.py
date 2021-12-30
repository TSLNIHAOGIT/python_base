# task_worker.py
import sys, time, queue
from multiprocessing.managers import BaseManager
from multiprocessing import Pool as ProcessPool

class QueueManager(BaseManager):
    pass


QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

local_ip = '192.168.10.13'
print('connect to server %s...' % local_ip)

m = QueueManager(address=(local_ip, 9833), authkey=b'abc')
m.connect()

task = m.get_task_queue()
result = m.get_result_queue()


# # num_cores = 1
# pool = ProcessPool(5)  # 设置池的大小
# pool.map_async(subAimFunc, args)




for i in range(100000):
    try:
        n = task.get(timeout=10)
        print('run task %d * %d' % (n, n))
        r = '%d * %d = %d' % (n, n, n * n)
        # time.sleep(1)
        result.put(r)
    except queue.Empty:
        print('task queue is empty')

print('worker exit')