# task_worker.py
import sys, time, queue
from multiprocessing.managers import BaseManager


class QueueManager(BaseManager):
    pass


QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

server_addr = '192.168.10.196'
print('connect to server %s...' % server_addr)

m = QueueManager(address=(server_addr, 9833), authkey=b'abc')
m.connect()

task = m.get_task_queue()
result = m.get_result_queue()

for i in range(10):
    try:
        n = task.get(timeout=10)
        print('run task %d * %d' % (n, n))
        r = '%d * %d = %d' % (n, n, n * n)
        time.sleep(1)
        result.put(r)
    except queue.Empty:
        print('task queue is empty')

print('worker exit')