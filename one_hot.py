
from sklearn import preprocessing
import numpy as np
label = preprocessing.LabelEncoder()
one_hot = preprocessing.OneHotEncoder(sparse = False)
cat_data =[[1,3,2]]
    # ,
    #        [2,1,1],
    #       [4,2,2]]
print (one_hot.fit_transform(cat_data))
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder

enc = OneHotEncoder()
data=np.array([[0, 0, 3], [1, 1, 0], [0, 2, 1],[1, 0, 2]])
data=pd.DataFrame(data)
print(data)
enc.fit(data)
print ("enc.n_values_ is:",enc.n_values_)
print ("enc.feature_indices_ is:",enc.feature_indices_)

res=enc.transform(data)
print (type(res),res[0][0])
print (enc.transform([[0, 1, 1]]).toarray())