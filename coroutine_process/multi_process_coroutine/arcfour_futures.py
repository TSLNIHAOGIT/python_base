import sys
import time
from concurrent import futures
from random import randrange
from coroutine_process.multi_process_coroutine.arcfour import arcfour

JOBS = 12
SIZE = 2**18

KEY = b"'Twas brillig, and the slithy toves\nDid gyre"
STATUS = '{} workers, elapsed time: {:.2f}s'


def arcfour_test(size, key):
    in_text = bytearray(randrange(256) for i in range(size))
    cypher_text = arcfour(key, in_text)
    out_text = arcfour(key, cypher_text)
    assert in_text == out_text, 'Failed arcfour_test'
    return size


def main(workers=None):
    if workers:
        workers = int(workers)
    t0 = time.time()

    ## 创建一个最大可容纳workers个task的线程池
    with futures.ProcessPoolExecutor(workers) as executor:
        t00 = time.time()
        actual_workers = executor._max_workers
        to_do = []
        for i in range(JOBS, 0, -1):
            size = SIZE + int(SIZE / JOBS * (i - JOBS/2))
            ## 往线程池里面加入一个task，返回future对象，对于Future对象可以简单地理解为一个在未来完成的操作。
            job = executor.submit(arcfour_test, size, KEY)
            to_do.append(job)

        for future in futures.as_completed(to_do):
            res = future.result()
            print('{:.1f} KB'.format(res/2**10))
        print(STATUS.format(actual_workers, time.time() - t00))

    print(STATUS.format(actual_workers, time.time() - t0))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        workers = int(sys.argv[1])
    else:
        workers = 1
    main(workers)
    '''
    1 workers, elapsed time: 6.07s
2 workers, elapsed time: 3.29s
3 workers, elapsed time: 2.63s
4 workers, elapsed time: 2.43s
5 workers, elapsed time: 2.41s
6 workers, elapsed time: 2.25s
7 workers, elapsed time: 2.33s
8 workers, elapsed time: 2.30s


6.07 3.29 2 workers 1.8449848024316111
6.07 2.63 3 workers 2.307984790874525
6.07 2.43 4 workers 2.4979423868312756
6.07 2.41 5 workers 2.5186721991701244
6.07 2.25 6 workers 2.697777777777778
6.07 2.33 7 workers 2.6051502145922747
6.07 2.3 8 workers 2.6391304347826092
384.0 KB
362.7 KB
341.3 KB
320.0 KB
298.7 KB
277.3 KB
256.0 KB
234.7 KB
213.3 KB
192.0 KB
170.7 KB
149.3 KB
    '''
