from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import PolynomialFeatures
from sklearn.datasets import  load_iris
iris=load_iris()
def poly_transform():

    print(iris.data[0:5])
    #多项式转换
    #参数degree为度，默认值为2
    data_new=PolynomialFeatures().fit_transform(iris.data)
    print(data_new[:5])


#基于单变元函数的数据变换可以使用一个统一的方式完成，使用preproccessing库的FunctionTransformer对数据进行对数函数转换的代码如下：from numpy import log1p
from sklearn.preprocessing import FunctionTransformer
from numpy import log1p
#自定义转换函数为对数函数的数据变换
#第一个参数是单变元函数
data_log=FunctionTransformer(log1p).fit_transform(iris.data)
print('data_log',data_log)

