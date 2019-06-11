import pandas as pd
df=pd.DataFrame()
df2=pd.DataFrame(data=[[1,2],[3,4]],columns=['x1','x2'])
print(df.append(df2))##append之后要赋值给df,因为原来的df并没有改变
print(df)