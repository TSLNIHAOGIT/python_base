import string
item = 'This is a demo.。'
# print(item[0:-1])
item = item.strip(string.punctuation)
item=item.strip('。')
print(item)
item=item.strip('。')
print(item)