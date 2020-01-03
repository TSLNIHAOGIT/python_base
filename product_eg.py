from itertools import product
print(list(product(['a','b','c'],['d','e','f'],['m','n'])))
for x,y,z in product(['a','b','c'],['d','e','f'],['m','n']):
    print(x,y,z)