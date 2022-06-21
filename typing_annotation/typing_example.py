from typing import List, Tuple, Dict,Optional,Union
def add(a:int, string:str, f:float, b:bool) -> Tuple[List, Tuple, Dict, bool]:
    list1 = list(range(a))
    tup = (string, string, string)
    d = {"a":f}
    bl = b
    return list1, tup, d,bl
print(add(5,"hhhh", 2.3, False))
# 结果：([0, 1, 2, 3, 4], ('hhhh', 'hhhh', 'hhhh'), {'a': 2.3}, False)

# 使用or关键字表示多种类型
def func(a:int, string:str) -> List[int or str]:
    list1 = []
    list1.append(a)
    list1.append(string)
    return list1
res = func(123,'hello')
print(res)


# Optional[int] 等价于 Union[int, None]#必须是int或者None
# 意味着：既可以传指定的类型 int，也可以传 None
def foo_func(arg: Optional[int]=None):
    print(arg)


foo_func()
foo_func(1)


# # 输出结果
# None
# 1
