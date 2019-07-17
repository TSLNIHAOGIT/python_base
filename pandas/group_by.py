import pandas as pd
import numpy as np
df=pd.DataFrame([[1,2],[3,5],[1,2],[5,4],[3,2],[3,4]],columns=['a','b'])
print(df)
# print(df.groupby(['a'])['b'].count().reset_index())
df_new=df.groupby(['a'])['a'].count()#.rename(columns={0:'a_count'})
print(type(df_new),'\n',df_new.index,df_new.values)
print(df_new.to_frame().rename(columns={'a':'a_count'}).reset_index())
# print(df.groupby(['a'])['b'].size().reset_index())

def count_encode(X, categorical_features, normalize=True):
    ##不需要join
    print('Count encoding: {}'.format(categorical_features))
    X_ = pd.DataFrame()
    for cat_feature in categorical_features:
        X_[cat_feature] = X[cat_feature].astype(
            'object').map(X[cat_feature].value_counts())
        if normalize:
            X_[cat_feature] = X_[cat_feature] / np.max(X_[cat_feature])
    X_ = X_.add_suffix('_count_encoded')
    if normalize:
        X_ = X_.astype(np.float32)
        X_ = X_.add_suffix('_normalized')
    else:
        X_ = X_.astype(np.uint32)
    return X_

count_encoding=count_encode(X=df, categorical_features=['a'], normalize=True)
print(count_encoding)