import pandas as pd
df=pd.DataFrame(data=[['a',1],['b',2]],columns=['v1','v2'])
print(df.head())
df['v11']=df['v1'].map({'a':'11','b':'22'})
print(df)