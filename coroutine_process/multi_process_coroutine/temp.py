import math
NUMBERS=range(12)
def chunks(l, size):

    n = math.ceil(len(l) / size)

    for i in range(0, len(l), n):

        yield l[i:i + n]
res=[ chunked for chunked in chunks(NUMBERS, 3)]
print('res',res)
JOBS=12
res=[each for each in range(JOBS, 0, -1)]
print(res)

print(['wwww,ax']*25)