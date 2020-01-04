import numpy as np
import time
s=time.time()
# print(np.power(20,10))
# r1=np.dot(np.random.random((7000,1000)),np.random.random((1000,7000)))
# r2=np.dot(np.random.random((7000,1000)),np.random.random((1000,7000)))
# res=r1+r2
# print(time.time()-s)
s=6.07
e=[3.29,2.63,2.43,2.41,2.25,2.33,2.30]
for index,each in enumerate(e):
    print(s,each,index+2,'workers',s/each)
