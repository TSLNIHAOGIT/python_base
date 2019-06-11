import queue

q = queue.Queue()

for i in range(5):
    #值放入队列
    q.put(i)

while not q.empty():
    #队列中取值，并输出
    print (q.get())