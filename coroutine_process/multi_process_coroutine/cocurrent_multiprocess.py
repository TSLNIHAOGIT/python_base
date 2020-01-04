import concurrent.futures
from concurrent import futures
import math
import numpy as np
import  time
PRIMES = [
    7771122725350952939999977777,
    7771099726899277333,
7771122725350952939999977777,
    7771099726899277333,
7771122725350952939999977777,
    7771099726899277333,
7771122725350952939999977777,
    7771099726899277333,
# 10000103,
# 100001037771099726899277333,
# 777109972689927733310000103,
# 777109972610000103899277333,
    # 777112582705942177777771733,
    # 77771122725350952939999977777,
    # 77777777115280095190777777737,
    # 7771157978480770999999977777,
    ]
num=range(4)
def compute_dot(num):
    if num:
        res=np.dot(np.random.random((7000, 1000)), np.random.random((1000, 7000)))
    return res

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def main():
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        # for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
        #     print('%d is prime: %s' % (number, prime))
        s1=time.time()
        for number, prime in zip(num, executor.map(compute_dot, num)):
            print('%d is prime: %s' % (number, 'e'))
        print('cost cc tt',time.time()-s1)
        # it_ls = []
        # for each in num:
        #     future = executor.submit(compute_dot)
        #
        # # for each in PRIMES:
        # #     future = executor.submit(is_prime, each)
        #     print(future.done())
        #     print('future',each, future)
        #     it_ls.append(future)
        # print('it_ls', it_ls)
        # done_iter = futures.as_completed(it_ls)  # as_completed()返回迭代器
        # print(done_iter)
        # for index, x in enumerate(done_iter):  # x是future对象
        #     print('res',index, x.result())


if __name__=='__main__':
    main()

'''
多个核心同时高负荷运转要：
1.任务数大于核心数，不然有的一直空闲在那
2.每个核心上的任务都是cpu密集型的，不然一下算出来后，然后会空闲
3.即使每个核心的任务都是cpu密集型，也由于任务，进程调度等原因，可能4个进程才是1个进程性能的2倍
'
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



'


'''