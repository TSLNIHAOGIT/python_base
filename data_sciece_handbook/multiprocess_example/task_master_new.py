import random, time, queue
from multiprocessing.managers import BaseManager

task_queue = queue.Queue()
result_queue = queue.Queue()

def task_queue_func():
    return task_queue
def result_queue_func():
    return result_queue

class QueueManager(BaseManager):
    pass


if __name__ == '__main__':
    print("master start.")
    QueueManager.register('get_task_queue', callable=task_queue_func)
    QueueManager.register('get_result_queue', callable=result_queue_func)
    manager = QueueManager(address=('192.168.10.13', 9833), authkey=b'abc')
    manager.start()
    task = manager.get_task_queue()
    result = manager.get_result_queue()

    for i in range(10):
        n = random.randint(0, 1000)
        print('put task %d ...' % n)
        task.put(n)
    print('try get results...')

    for i in range(10):
        r = result.get(timeout=1000)
        print('Result:%s' % r)
    manager.shutdown()
    print('master exit.')