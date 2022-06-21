from typing import Sequence as Seq1
from typing import List,Tuple,Literal,Union,Dict

#是并集的意思，整形或者字符串都可以？？
a:List[Union[int,str]] = ['a',123]

##这里似乎只要有整形就可以，而不是全部都是整形
a2:list[int] = [123,'a','123']

a2:dict[int] = ['a','123']
a3:dict[int] = [123,345]



MODE = Literal['r', 'rb', 'w', 'wb']
mode:MODE = 123

age :int = '123'
weight : float = 123.7
ages:List[int] = ('123','456')

data3:List[int]=[12,'123']
data4:Dict[str,int]={'a':'b','b':'c'}
data:tuple[int]=(12,'123')
data2:Tuple[int]=(12,24)

scores: list[int]
ages2: dict[str, int] = {'1':'hg','w':123}

mydata:Seq1[str] = ['1','2','3']
mydata2:Seq1[str] = [1,2,3]