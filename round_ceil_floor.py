
import math
import numpy as np
# 向上取整
print(math.ceil(3.1))

# 向下取整
print(math.floor(3.7))

#四舍六入五成双：五成双即及时
'''
①.当被修约的值为5时，如果他前面的数为偶数且被修约数的后面没有数时则舍弃；
②.当被修约的值为5时，如果他前面的数为偶数时且被修约数的后面还有数时，则进位。
③.当被修约的值为5时，如果他前面的数为奇数时则进位；

被修约的数字等于5时，要看5前面的数字，
    若是奇数则进位，
    若是偶数则将5舍掉，即修约后末尾数字都成为偶数；
    若5的后面还有不为“0”的任何数，则此时无论5的前面是奇数还是偶数，均应进位。
'''
print(round(22.5))
print(round(22.51))

print(round(23.5))
print(round(22.51))

#四舍五入方法
# 1.扩大100倍然后缩小100

# 2.用decmicial模块
from _pydecimal import Decimal, Context, ROUND_HALF_UP
print(Context(prec=4, rounding=ROUND_HALF_UP).create_decimal('0.3255'))

#利用’’%.af’’%b——其中 b 代表要限定的数字， a 代表要求限定小数点的位数，结果自动四舍五入。
c = 1.264871331241212
data=[22.5555,22.5551,23.5555,23.5551]
for each in data:
    print("%.3f"%each)

print(np.round(data,decimals=3))