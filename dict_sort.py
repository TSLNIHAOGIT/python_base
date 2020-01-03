#python3.6开始dict已经变得有序


# data_dict={1:3,2:4,6:8,3:5,9:7,12:8}
data_dict={'&': 5, 'China': 4, 'Loading': 1, 'Place': 2, 'To': 0}
print(data_dict.keys())
dd=data_dict.items()
dd=sorted(dd,key=lambda x:x[1])
print('dd',dd)
print('redict',dict(dd).keys())
def list_sort():
    data= [(3, 66), (5, 3), (1, 23)]
    data.sort()#默认以元祖的第一个元素排序
    print(data)
    data = [(3, 66), (5, 3), (1, 23)]
    data.sort(key = lambda item:item[1])  # 按照第二个元素排序
    print(data)
def sorted_data():
    data = [(3, 66), (5, 3), (1, 23)]
    sd=sorted(data,reverse=False)#默认以第一个元素排序
    print(sd)

    #以第二个元素排序
    sd = sorted(data,key=lambda item:item[1],reverse=False)
    print(sd)


if __name__=='__main__':
    # list_sort()
    sorted_data()