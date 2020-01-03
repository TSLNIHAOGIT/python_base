from goto import with_goto


# @with_goto
# def range(start, stop):
#     i = start
#     result = []
#
#     label.begin
#     if i == stop:
#         goto.end
#
#     result.append(i)
#     i += 1
#     goto.begin
#
#     label.end
#     return result
#
# res=range(start=10, stop=10)
# print(res)
# def go_to():
#     print('你好')

def tt():
    def go_to():
        print('你好')
        return
    for each in range(20):
        if each<15:
           print(each)
        else:
            yield go_to
tt()
