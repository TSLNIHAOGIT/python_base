def func1(a,b):
	return a/b
	
def func2(x):
	a=x
	b=x-1
	return func1(a,b)
		
def func3(x):
	a=x
	b=x-1
	return func2(x)
	