from collections import  deque
a=deque(['a','b','c'],maxlen=2)
#结果之所以是deque([2, 3])，是因为首先1进队，然后2进队，最后3进队，数据溢出，1消失
print(a)
'''
append：同list的append，在队尾加入一个元素

appendleft:在队首加入一个元素

clear：清空队列

copy：浅拷贝，b=a.copy(),关于深浅拷贝的区别，浅拷贝复制的是引用，深拷贝的话复制的是不可变元素的引用和可变元素的复制；我觉得一篇文章写得特别好，请关注https://blog.csdn.net/qq_32907349/article/details/52190796

count：a.count(1),a中1的数量

entend：参数是一个可迭代变量，在右端按照迭代顺序添加

extendleft：同上，不过是在左端按照迭代顺序添加，如下图
'''
a=deque(['a','b','c'])

#结果之所以是deque([2, 3])，是因为首先1进队，然后2进队，最后3进队，数据溢出，1消失
print(a)
# a.extend([2,3,4])#添加右边第一个、第二个等按照迭代顺序
# print(a)
a.extendleft([2,3,4])#添左边第一个、第二个等按照迭代顺序
print(a)

b=deque()
b+=['a','b','c']
print(len(b),b)
print(b.popleft())
print(b.popleft())
b.append('哈哈')
print(b)