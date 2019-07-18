sentence='Indeed , Brazi many Brazilians blame Bolivia and its president ,pres  Evo Morales , for much of the energy squeeze their country is beginning to feel , in the form of higher prices for natural gas and uncertainties about future supplies '
import re
# re.escape(pattern) 可以对字符串中所有可能被解释为正则运算符的字符进行转义的应用函数。
# 如果字符串很长且包含很多特殊技字符，而你又不想输入一大堆反斜杠，或者字符串来自于用户(比如通过raw_input函数获取输入的内容)，且要用作正则表达式的一部分的时候，可以使用这个函数。
print(re.escape('www.com.cn.'))
def multiple_replace(text, adict):
     print(list(map(re.escape, adict)))
     #map(func,iter_obj)func对迭代对象的每个元素进行操作

     #就是构建了正则表达式
     rx = re.compile('|'.join(map(re.escape, adict)))
     # print('rx',rx)
     def one_xlat(match):
           print('match:',match.group(0))
           return adict[match.group(0)]
     #参数是函数时的用法
     return rx.sub(one_xlat, text)
print(multiple_replace(sentence,{'Brazi ':'Brazi-loc ','pres ':'pres_s '}))


import re
def dashrepl(matchobj):
     print(matchobj.group())
     if matchobj.group(0) == '-':
           return '***'
     else:
           return '+++'
print(re.sub('-{1,2}', dashrepl, 'pro-----gram---files'))

print(re.sub(r'\sAND\s', ' & ', 'Baked Beans And Spam', flags=re.IGNORECASE))
# 'Baked Beans & Spam')

input_data='0:品牌类型1:出口享惠情况2:稀土元素的重量百分比,以[A]表示3:GTIN4:CAS'
def fun(match):
    # if match.group(0)=='1:':
    #     return '1111'
    # else :
    #     return '0000'
    return '{}_**'.format(match.group(0))

print(re.sub('\d:',fun,input_data))