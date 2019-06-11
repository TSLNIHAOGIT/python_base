mailto = ['cc', 'bbbb', 'afa', 'sss', 'bbbb', 'cc', 'shafa']

addr_to = list(set(mailto))
print(addr_to)
addr_to.sort(key = mailto.index)
print(addr_to)