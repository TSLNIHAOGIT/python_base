import pandas as pd
import numpy as np
df=pd.DataFrame([[1,2],[3,5],[1,2],[5,4],[5,4]],columns=['a','b'])
print(df)
# print(df.groupby(['a'])['b'].count().reset_index())
df_new=df.groupby(['a'])['a'].count()#.rename(columns={0:'a_count'})
print(type(df_new),'\n',df_new.index,df_new.values)
print(df_new.to_frame().rename(columns={'a':'a_count'}).reset_index())
# print(df.groupby(['a'])['b'].size().reset_index())


features=['a','b']
temp = df.groupby(features).count().reset_index().rename(columns={0: 'new_feature'})
print('t1',temp)


temp = df.groupby(features).size().reset_index().rename(columns={0: 'new_feature'})
print(temp)
def count_encode(X, categorical_features, normalize=True):
    ##不需要join
    print('Count encoding: {}'.format(categorical_features))
    X_ = pd.DataFrame()
    for cat_feature in categorical_features:
        X_[cat_feature] = X[cat_feature].astype(
            'object').map(X[cat_feature].value_counts())###里面其实是一个字典映射了
        if normalize:
            X_[cat_feature] = X_[cat_feature] / np.max(X_[cat_feature])
    X_ = X_.add_suffix('_count_encoded')
    if normalize:
        X_ = X_.astype(np.float32)
        X_ = X_.add_suffix('_normalized')
    else:
        X_ = X_.astype(np.uint32)
    return X_

count_encoding=count_encode(X=df, categorical_features=['a'], normalize=False)
print(count_encoding)
print(df['a'].value_counts().to_dict())
print(df['a'].unique())
print(df['a'].nunique())

# features=['a','b','c']
# new_feature = 'count'
# nunique = []
# for i in features:
#     # nunique.append(data[i].nunique())
#     new_feature += '_' + i.replace('add_', '')
#     print(new_feature)

count_feature_list=[]
def feature_count(data, features=[], is_feature=True):
    if len(set(features)) != len(features):
        print('equal feature !!!!')
        return data
    new_feature = 'count'
    nunique = []
    print('new_feature',new_feature)
    for i in features:
        nunique.append(data[i].nunique())
        new_feature += '_' + i.replace('add_', '')
        print('new_feature', new_feature)

    # 不只一个特征名称	      该dataframe去掉重复行后的条数<=每个特征的nunique值中的最大值：就是行数小于等于某个特征的最大类别数
    # 小于号不可能取到，最多是等于号，因为单个列去重条数一定是大于等于多个列去重，所以这里最多是等于
    print(len(data[features].drop_duplicates()) , np.max(nunique))
    if len(features) > 1 and len(data[features].drop_duplicates()) <= np.max(nunique):
        print(new_feature, 'is unvalid cross feature:')
        return data #返回后面的就不会继续运行
    temp = data.groupby(features).size().reset_index().rename(columns={0: new_feature})
    data = data.merge(temp, 'left', on=features)
    if is_feature:
        count_feature_list.append(new_feature)
    print('count_feature_list',count_feature_list)
    if 'day_' in new_feature:
        print('fix:', new_feature)
        ##第三天采样比过低，所以增加了权重
        data.loc[data.day == 3, new_feature] = data[data.day == 3][new_feature] * 4
    return data

feature_count(data=df, features=['a','b'], is_feature=True)