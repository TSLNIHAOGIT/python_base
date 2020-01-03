#encoing=utf8
import pandas as pd
import matplotlib.pyplot as plt
#路径要加r不然读取时有问题
path=r'F:\陶士来文件\tsl_python_project\python_base\rpa_test\process_monitor_waitress-serve_20298_test0.csv'
path=r'F:\陶士来文件\tsl_python_project\python_base\rpa_test\process_monitor_waitress-serve_33049_test01.csv'



df=pd.read_csv(path,encoding='utf8')
df['time_new']=df['time'].apply(lambda x:x.split('-')[1])
time=df['time_new']
cpu=df['cpu%']
mem=df['mem%']
print(df.describe())
print(df.head())
#中文无法显示问题
# plt.figure('第一个图片')
plt.plot(time,cpu,label='time-cpu')
# plt.figure('第二个图片')
# plt.plot(time,mem,label='time-mem')
# plt.figure('第二个图片')
plt.xticks(time, time, rotation=90)
# 设置横纵坐标的名称以及对应字体格式
font2 = {'family': 'Times New Roman',
         'weight': 'normal',
         'size': 1,
         }
plt.xlabel('时间', font2)
plt.ylabel('ration', font2)
plt.tick_params(labelsize=10)
# plt.rcParams['font.sans-serif'] = ['SimHei']#可以plt绘图过程中中文无法显示的问题
plt.legend()#显示图例，如果注释改行，即使设置了图例仍然不显示

plt.show()

import matplotlib.pyplot as plt

# if __name__ == '__main__':
#     x = ["1234", "2345", "5678", "6789", "7890"]
#     y = [1, 2, 3, 4, 5]
#     # plt.bar(x, y, width=0.35)
#     plt.plot(x,y)
#     plt.xticks(x, x, rotation=30)  # 这里是调节横坐标的倾斜度，rotation是度数
#     # 显示柱坐标上边的数字
#     # for a, b in zip(x, y):
#     #     plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=17)  # fontsize表示柱坐标上显示字体的大小
#     plt.show()
