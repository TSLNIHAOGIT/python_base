def foo():
    while True:
        x = yield
        print("value:",x)

g = foo() # g是一个生成器
print('next_g1')
next(g) # 程序运行到yield就停住了,等待下一个next

g.send(1)  # 我们给yield发送值1,然后这个值被赋值给了x，并且打印出来,然后继续下一次循环停在yield处
# g.send(2)  # 同上
#
print('next_g2')
next(g)  # 没有给x赋值，执行print语句，打印出None,继续循环停在yield处