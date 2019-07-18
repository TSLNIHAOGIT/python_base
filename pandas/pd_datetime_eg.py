# time_data=1.560174e+12
time_data=1560174000000.0 #(ms)
print(time_data)
import pandas as pd
from datetime import datetime,timedelta
import time

# 对时间的处理
# all_data['time'] = pd.to_datetime(all_data['nginxtime']*1e+6) + timedelta(hours=8)
# all_data['day'] = all_data['time'].dt.dayofyear
# all_data['hour'] = all_data['time'].dt.hour
print(timedelta(hours=8))
###default 'ns',time_data单位是ms,是utc时间与北京时间相差8个小时,localtime()接收时间单位是s
tt1=pd.to_datetime(time_data*1e+6)+timedelta(hours=8)
print('tt1',tt1,'*',tt1.day,'8',tt1.year,tt1.hour)

tt2=pd.to_datetime(time_data+8*3600000,unit='ms')
print('tt2',tt2)


from time import strftime, localtime
print('rt1',strftime('%Y-%m-%d %H:%M:%S',localtime(time_data/1000)))
print('rt2',strftime("%d", time.localtime(time_data/1000)))
# print(time.localtime(seconds=time_data))
# day_tt=int(time.strftime("%d", time.localtime(time_data)))
# print('day_tt',day_tt)
# import time
# train['day'] = train['nginxtime'].apply(lambda x : int(time.strftime("%d", time.localtime(x))))
# train['hour'] = train['nginxtime'].apply(lambda x : int(time.strftime("%H", time.localtime(x))))