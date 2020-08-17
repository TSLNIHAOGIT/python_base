class listnode():
    """节点类型"""
 
    def __init__(self,data,next):
         """初始化节点构造函数"""
         self.data = data
         self.next = next
 
 
def create_lisklist(head):
        """创建链表"""

        r = head
        data = input("'#' means to quit! Please input a data:")
        while data != '#':
            p = listnode(data,None)#暂时将next指针设为空值
            r.next = p
            r = p
            p = p.next
            data = input("'#' means to quit! Please input a data:")

def printf(head):

     """打印链表"""


     p = head.next

     while p.next != None:

         print(p.data)

     p = p.next

     print(p.data)

def main():

    """主函数"""


    head = listnode('0', None)  # 构造头结点



    create_lisklist(head)  # 创建链表

    printf(head)  # 打印节点





if __name__=='__main__':
    main()