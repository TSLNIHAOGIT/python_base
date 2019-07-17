import pandas as pd
def map_eg():
    #map是python自带的，对某一列进行操作
    df=pd.DataFrame(data=[['a',1],['b',2]],columns=['v1','v2'])
    print(df.head())
    df['v11']=df['v1'].map({'a':'11','b':'22'})
    print(df)
def applymap_eg():
    #applymap对dataframe全部元素进行操作
    import pandas as pd
    import numpy as np

    frame = pd.DataFrame(np.random.rand(4, 3), columns=list('abc'), index=['Utah', 'Ohio', 'Texas', 'Oregon'])
    print(frame)
    # 输出如下:
    #                a         b         c
    # Utah    0.443188  0.919623  0.550259
    # Ohio    0.013923  0.557696  0.723975
    # Texas   0.865469  0.720604  0.081306
    # Oregon  0.506174  0.212421  0.061561

    func = lambda x: f'{x:.2f}%'
    print(frame.applymap(func))

    # 输出如下:
    #             a      b      c
    # Utah    0.34%  0.43%  0.67%
    # Ohio    0.75%  0.50%  0.14%
    # Texas   0.68%  0.28%  0.90%
    # Oregon  0.05%  0.86%  0.78%
if __name__=='__main__':
    applymap_eg()