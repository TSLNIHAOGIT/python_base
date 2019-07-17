import pandas as pd
df = pd.DataFrame({'区域1' : ['西安', '太原', '西安', '太原', '郑州', '太原'],
                   '区域2' : ['太1原', '太2原', '西3安', '西4安', '西6安', '太8原']})
# print(df.iloc[0:2])
print(df)

# print(df.apply(pd.value_counts).reset_index().rename(columns={'index':'name'}))##相当于两列是所有的唯一值作为name
print('hh',df['区域1'].apply(lambda x:pd.value_counts(x)))
print(pd.value_counts(df['区域1']).to_frame().reset_index().rename(columns={'index':'区域1','区域1':'area_count'}))

# train=pd.DataFrame([[1,2],[3,4]],columns=['v1','v2'])
# test=pd.DataFrame([[11,22],[33,44]],columns=['v1','v2'])
# test2=pd.DataFrame([[11,22],[33,44]],columns=['v11','v22'])
# tt=train.append(test,ignore_index=True)
# print(tt)
# print(tt['v1'].sample(4))
# print(pd.merge(tt,test2,right_index=True,left_index=True))