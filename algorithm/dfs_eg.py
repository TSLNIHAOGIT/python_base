import collections
import queue

g = collections.OrderedDict()
g['A'] = ['B', 'C', 'D']
g['B'] = ['A', 'E']
g['C'] = ['A', 'F']
g['D'] = ['A', 'G', 'H']
g['E'] = ['B', 'F']
g['F'] = ['E', 'C']
g['G'] = ['D', 'H', 'I']
g['H'] = ['G', 'D']
g['I'] = ['G']

def BFSTraverse(g):
    visited = {}
    #first in first out
    q = queue.Queue()

    for v in g:
        # #键不存在时返回None，此时输出新的键（顶点）
        if not visited.get(v):
            print('1:',v)
            #将新键加入字典中作为访问过的，值设为True
            visited[v] = True  # 先访问再入队

            #将该顶点放入队列
            q.put(v)

        #队列不为空时，先放进去的值，先取出来
        while not q.empty():
            e = q.get()

            #根据顶点取出邻接点
            #例如A的邻接点B、C、D
            for adj in g[e]:
                #邻接点没有访问过时（新的顶点），加入字典标记为访问过
                if not visited.get(adj):#键不存在时返回None
                    print('2:',adj)
                    visited[adj] = True

                    #将邻接点放入队列
                    q.put(adj)


"""
广度优先搜索
"""
# dict = {}
# dict["oysq"] = ["a", "b", "c"]
# dict["a"] = ["e", "f", "g"]
# dict["b"] = ["h", "i"]
# dict["c"] = []
# dict["d"] = []
# dict["e"] = []
# dict["f"] = []
# dict["g"] = []
# dict["h"] = ["j", "k"]
# dict["i"] = []
# dict["j"] = []
# dict["k"] = ["l"]
# dict["l"] = []


# def search(dict, head, target):
#     search_list = []
#     search_list += dict[head]
#     searched = []
#     while search_list != []:
#         temp = search_list.pop()
#         if searched.count(temp) == 0:
#             if temp == target:
#                 return True;
#             else:
#                 search_list += dict[temp]
#                 searched += temp
#     return False


from collections import deque

# 无权最短路径算法：广度优先搜索算法，求得通过点最少的路径

graph = {}
graph["you"] = ["alice", "bob", "claire"]
graph["bob"] = ["anuj", "peggy"]
graph["alice"] = ["peggy"]
graph["claire"] = ["anuj", "jonny"]
graph["anuj"] = ["tom"]
graph["peggy"] = []
graph["tom"] = []
graph["jonny"] = []

filter = {}
sign = ""


def test(query):
    global sign
    if (len(query) == 0):
        print(1)
        print("没有找到这个人")
    else:
        print(2)
        #从列表的左边开始取元素
        print('query',query)
        person = query.popleft()
        print('person:',person)
        # 取出的人加入过滤器，避免重复
        #邻接点加入字典作为访问过的
        filter[person] = 0
        # 判断是否为m结尾
        # if (person[-1] == 'm'):
        if (person == 'tom'):
            print(1.1)
            print(person + ": now you see me !")
            sign = person
            return person
        else:
            print(2.1)
            # 把这个人的邻居加入队列中,使用过滤器做判断，避免把拿出的人在放进去
            for i in graph[person]:
                #当邻接点是新的节点时，将加入队列中
                #即列表末尾加入新节点
                # print('i,filter:',i,filter)
                if not i in filter:
                    # print('query1',query)
                    query.append(i)
                    # #自己添加的,不添加就出错了，有的节点遍历两次
                    filter[i] = 0
                    # print('query2', query)

            #test是一个递归最后才返回一个值tom
            #找到Tom之后else不被执行，返回test的递归值继续运行
            print('query2',query)

            temp = test(query)
            print('temp',temp)
            print('sign',sign)
            if (sign in graph[person]):
                print('1.1.1')
                sign = person
                return person + "->" + temp
            else:
                print('2.1.1')
                return temp




if __name__=='__main__':
    # BFSTraverse(g)

    # visited = {}
    # print(visited.get('a'))#None

    # print(search(dict, "oysq", "c"))
    # print(search(dict, "oysq", "v"))


    # 定义队列，python deque表示一个可以前后入队出队的队列
    search_query = deque()
    # 先把起点的邻居加进队列
    search_query += graph["you"]
    print(test(search_query))