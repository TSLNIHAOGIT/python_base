import pyhdfs
#空的文件系统

from hdfs.client import Client
# fs = pyhdfs.HdfsClient(hosts="http://192.168.28.195")  # 这两种连接方式都可以

##格式语法有问题端口写50070 ，9000（似乎速度要慢），或者不写都可以连上
fs = pyhdfs.HdfsClient(hosts="192.168.28.195,50070")  # 这两种连接方式都可以

# fs = pyhdfs.HdfsClient(hosts="192.168.28.183")  # 这两种连接方式都可
# # # fs = pyhdfs.HdfsClient(hosts="192.168.130.163,9000", user_name="root")
# print('fs',fs)
print(fs.get_home_directory())
print (fs.get_active_namenode())


# fs=Client("192.168.28.183:50070")
# print(dir(fs))
# # print(fs.status('/'))
print(fs.listdir("/user"))

# # 打开一个远程节点上的文件，返回一个HTTPResponse对象
# response = fs.open("/user/local.txt")
#
# # 查看文件内容
# print('read content',response.read())
# #
# 从本地上传文件至集群
fs.copy_from_local( r"F:\陶士来文件\tsl_python_project\python_base\pyhdfs\wordcounts.txt",'/user/wordcounts.txt')

# 从本地上传文件至集群之后，集群的目录
print("After copy_from_local")
print(fs.listdir("/user"))
