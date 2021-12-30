import random, time, queue
from multiprocessing import Manager, Pool
from multiprocessing.managers import BaseManager

task_queue = queue.Queue()
result_queue = queue.Queue()

def task_queue_func():
    return task_queue
def result_queue_func():
    return result_queue

class QueueManager(Manager):
    pass


if __name__ == '__main__':
    print("master start.")
    local_ip = '192.168.10.13'
    QueueManager.register('get_task_queue', callable=task_queue_func)
    QueueManager.register('get_result_queue', callable=result_queue_func)
    manager = QueueManager(address=(local_ip, 9833), authkey=b'abc')
    manager.start()
    task = manager.get_task_queue()
    result = manager.get_result_queue()
    print('manager.address',manager.address)


    for i in range(10):
        # n = random.randint(0, 1000)
        n = i
        print('put task %d ...' % n)
        task.put(n)
    print('try get results...')

    print(result.wait)
    for i in range(100000):
        r = result.get(timeout=100000)
        print('Result:%s' % r)
    manager.shutdown()
    print('master exit.')