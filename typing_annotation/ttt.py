sortList = ["4","3","5","2","1"]

# 当前列表

curList = [{"id":"1","province":"河南"},{"id":"2","province":"河北"},{"id":"3","province":"湖南"},{"id":"4","province":"湖北"},{"id":"5","province":"江西"}]

# 根据指定列表中的ID顺序，对当前列表进行排序

curList = sorted(curList,key = lambda item:sortList.index(item["id"]))

print(curList)