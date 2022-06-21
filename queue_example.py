import queue
queue.Queue()
q1 = queue.Queue()
a={'1':{'q':1},'2':{'w':2},'3':{'e':4}}
a1=list(a.items())
for each in a1:
    q1.put(each)
pass