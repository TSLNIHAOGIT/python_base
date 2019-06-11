#Author:wang yue

def f1():
    a=3
    b=2
    for i in range(3):
        #加try异常判断，整个循环过程就会执行到底；如果不加，遇到异常就会退出运行；
        #但是try里面，报错之后剩下的语句就没有执行了。
        print('i={}'.format(i))
        try:
            a = a - 1
            c=b/1
            print('哈哈')
            # print(c)

        except Exception as e:
            print('e',e)
        except Exception as e2:
            print('e2',e2)
        else:
            #发生异常时，else的语句没有被运行
            print("正常运行")
        finally:
            #无论异常是否发生，在程序结束前，finally中的语句都会被执行。
            print("finally")
        
        
def safe_float(obj):
   try:
      return float(obj)
   except ValueError:
      retval = 'could not convert non-number to float'
      print (retval)
   except TypeError:
      retval = 'object type cannot be converted to float'
      print(retval)


def safe_float2(obj):
     try:
        return float(obj)
     except (ValueError, NameError, TypeError):
        retval = 'object type cannot be converted to float'
        print(retval)
        return retval
   
if __name__=='__main__':
    # safe_float(int)
    # safe_float2('')
    f1()
