import traceback
import sys

def eg(k):
    a=[1,2,3,0,4,5]
    print(k,a[k],k/a[k])





def main():

    try:
        for i in range(6):
            eg(i)

    except Exception as e:
        print('err',e)
        # print(sys._getframe().f_lineno, 'str(e):\t\t', str(e))
        # print(sys._getframe().f_lineno, 'repr(e):\t', repr(e))
        # print(sys._getframe().f_lineno, 'e.message:\t', e)
        # print(sys._getframe().f_lineno, 'traceback.print_exc():')
        traceback.print_exc()
        print(sys._getframe().f_lineno, 'traceback.format_exc():\n%s' % traceback.format_exc())
        return e


if __name__=='__main__':
   e= main()
   print('get err:',e)