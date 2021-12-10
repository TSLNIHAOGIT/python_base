from collections import defaultdict
# res=defaultdict(list,3)
# print(res)
# for i in range(3):
#     print(res[i])
#     res[i] = str(i)
# print(res)

def log_missing():
    print('key added')
    return 100
current = {'green':12,'blue':3}
increments = [('red',5),('blue',17),('orange',9)]

#意思是根据字典中键取值时，如果键存储就取对应的只，否则默认值为函数返回的值
result = defaultdict(log_missing,current)
print('raw result',result)
print('before',dict(result))
for k,a in increments:
    print(f'{k}',result[k])
    result[k] += a
print('after:',dict(result))
# after: {'green': 12, 'blue': 20, 'red': 105, 'orange': 109}
#