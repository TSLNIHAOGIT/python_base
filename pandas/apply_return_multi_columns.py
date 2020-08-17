import pandas as pd
import  numpy as np
df = pd.DataFrame(data = {'a': [1, 2, 3],
                          'b': [4, 5, 6]})




def add_subtract(a, b):
  return (a + b, a - b)

def add_subtract_list(a, b):
  '''
  要返回一个series才可以，需要index信息，否则报如下错误
  KeyError: "None of [Index(['sum_list', 'difference_list'], dtype='object')] are in the [columns]"
  :param a:
  :param b:
  :return:
  '''
  return pd.Series([a + b, a - b])


def add_subtract_series(a, b):
  # print('pd.Series\n',pd.Series((a + b, a - b)))
  return pd.Series((a + b, a - b))

df[['sum_series', 'difference_series']] = df.apply(
    lambda row: add_subtract_series(row['a'], row['b']), axis=1)

df[['sum_list', 'difference_list']] = df.apply(
    lambda row: add_subtract_list(row['a'], row['b']), axis=1)



df[['sum', 'difference']] = df.apply(
    lambda row: pd.Series(add_subtract(row['a'], row['b'])), axis=1)


if __name__=='__main__':
    print(df)