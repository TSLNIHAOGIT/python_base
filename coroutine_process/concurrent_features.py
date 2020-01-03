from concurrent import futures
import time
import numpy  as np

def f(x):
    # print('start flag', flag)
    #
    # if flag:

        # np.dot(np.random.random((5000, 2000)), np.random.random((2000, 5000)))
    print('x in',x)
    data=np.power(x,2)
    time.sleep(0.5)
    print('data out',data)
    return data


def test_func(n):
    print(f"{n} starts!")
    # for i in range(n):
    #     time.sleep(0.5)
    return f"n = {n} completed!"


def test(max_workers=4):
    with futures.ThreadPoolExecutor(max_workers) as executor:
        list1 = [ f(x) for x in range(1, max_workers+1)]
        # it is a iterator of results.
        it = executor.map(test_func, list1)
        print(it)
        for x in  it:
            print(x)
def test_2(max_workers=4):
    with futures.ProcessPoolExecutor(max_workers) as executor:
    # with futures.ThreadPoolExecutor(max_workers) as executor:
    #     list1 = [f(x,y) for x,y in zip(range(1, max_workers+1),[True,False,False,True])]
        it_ls = []
        # for x in list1:
            # e=np.random.rand()
            # flag=[True if e>0.5 else False][0]
            # print(flag)

            # future = executor.submit(test_func, x) # 返回一个future


        for each in [20,5,10000000,2]:
            future=executor.submit(f,each)
            print(future.done())
            print('future',future)
            it_ls.append(future)
        print('it_ls',it_ls)
        done_iter = futures.as_completed(it_ls)  # as_completed()返回迭代器
        print(done_iter)
        for x in done_iter: # x是future对象
            print('res',x.result())
'''
实现异步IO必须有IO操作（如time.sleep等），然后交出控制权，然后进行异步？？
x in 20
x in 5
x in 10000000
x in 2

data out 400
res 400
data out 276447232
data out 25
res 276447232
res 25
data out 4
res 4

'''

if __name__ == "__main__":
    m_workers = 10
    # test(m_workers)
    test_2(max_workers=8)