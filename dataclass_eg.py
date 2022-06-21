from dataclasses import  dataclass
from typing import Optional,Tuple,List,Dict,Set,AbstractSet



# Set、集合，是 set 的泛型；AbstractSet、是 collections.abc.Set 的泛型。根据官方文档，Set 推荐用于注解返回类型，AbstractSet 用于注解参数。它们的使用方法都是一样的，其后跟一个中括号，里面声明集合中元素的类型，如：
# 这里将 Set 用作了返回值类型注解，将 AbstractSet 用作了参数类型注解。

def describe(s: AbstractSet[int]) -> Set[int]:
    return set(s)


ships:AbstractSet[int] = {1}

print('ships',ships)


@dataclass()
class Boat:
    '''一条船的数据结构'''
    id:str
    allow_lift:str
    category:str
    length:float
    width:float


    # arrangement_coordinate:Optional[Tuple[float,float]]
    # fronted_coordinate:Optional[Tuple[float,float]]
@dataclass()
class BoatSeq:
    boat_seq:Dict[str,'Boat']

@dataclass()
class Lock:
    length: float
    width: float


@dataclass()
class ArangementedLock:
    '''排布过后的一闸船'''
    #一闸的利用率
    usage:float
    #该闸的可排点
    available_seq:List[Tuple[float,float]]

    #排好的一闸船;这里有些问题，排好的一闸中船有对应的坐标
    # lock_boats:Dict[str,'Boat']


class ArrangeLock:
    def __init__(self,boat_seq:'BoatSeq',lock:'Lock'):
        self.boat_seq = boat_seq
        self.lock = lock
    def arranage_lock(self,boat_seq,lock):

        pass



if __name__ == '__main__':
    boat=Boat(
        id='106606783950225408',
       allow_lift= '0',
       category= '1005',
       length= 65,
       width=10)

    # boat = Boat('106606783950225408','0','1005',65,10)
    pass




