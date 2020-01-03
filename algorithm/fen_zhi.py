#-*- coding:utf-8 -*-
#分治法求解最大值问题
import random
#求解两个元素的列表的最大值方法
def max_value(max_list):
  return max(max_list)
#定义求解的递归方法
def solve(init_list):
  if len(init_list) <= 2:
  #若列表元素个数小于等于2，则输出结果
    print(max_value(init_list))
  else:
    init_list=[init_list[i:i+2] for i in range(0,len(init_list),2)]
    print(init_list)
    #将列表分解为列表长度除以2个列表
    max_init_list = []

    #用于合并求最大值的列表
    for _list in init_list:
    #将各各个子问题的求解列表合并
      max_init_list.append(max_value(_list))
    print('max', max_init_list)
    solve(max_init_list)
if __name__ == "__main__":
  test_list = [12,2,23,45,67,3,2,4,45,63,24,23,28]
  #测试列表
  solve(test_list)