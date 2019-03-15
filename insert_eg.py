a=[1,2,3,4]
a.insert(0,'c')
a.insert(0,'d')
print(a)
class Node(object):
    def __init__(self,value,next):
        self.value=value
        self.next=next
a=Node(1,Node(2,Node(3,Node(4,None))))
print(a)
print(a.value)
print(a.next.value)
print(a.next.next.value)
print(a.next.next.next.value)