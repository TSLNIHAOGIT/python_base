from easygui import *
aa=int(input(""))
if aa==1:
    a=int(input("首项:"))
    b=int(input("末项:"))
    c=int(input("公差:"))
    d=(b-a)/c+1
    e=(a+b)*d/2
    print(d)
if aa==2:
    msgbox("请在下面程序中输入要加密的东西","2")
    e=input("字:")
    f=ord(e)
    g=f+513
    h=chr(g)
    msgbox("结果是：" + h,"2")
    print(h)
if aa==3:
    i=input("字:")
    j=ord(i)
    k=j-513
    l=chr(k)
    print(l)
if aa==4:
    print("欢迎来到杀迷你OS!!!")
    m = input("确定启用（确定输入S，退出输入Q）：")
    def a(m):
        if m == "S":
           pass
        else:
          quit()
    for n in range(101):
        print("处理中......",n,"%")
quit()