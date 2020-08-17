def a():
    print("error")
    a()
# a()
print(set([(199, 198), (198, 178)]))
list_eg=[{198}&set(each)  for each in [(199, 198), (198, 178)] if {198}&set(each)]
print(bool(list_eg))

from sklearn.datasets import load_iris, load_boston,load_iris
from xgboost import XGBClassifier,XGBRegressor
boston = load_boston()
train = pd.DataFrame(boston['data'])
label = pd.Series(boston['target'],name='label')
full = pd.concat((train,label),axis=1)
model = XGBRegressor(n_estimators=3,max_depth=1,reg_lambda=0,reg_alpha=0)
model.fit(train,label)
model.predict()
model.get_booster().trees_to_dataframe()