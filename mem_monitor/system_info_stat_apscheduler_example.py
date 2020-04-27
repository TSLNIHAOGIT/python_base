import time
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import sys
import time
import psutil
import GPUtil
Gpus = GPUtil.getGPUs()
gpu_amount=len(Gpus)
def gpu_monitor():
    # 获取多个GPU的信息，存在列表里
    all_gpus_stats=[]
    for gpu in Gpus:
        gpu_id=gpu.id
        gpu_memorytotal=gpu.memoryTotal
        gpu_memoryUsed=gpu.memoryUsed
        gpu_percent=gpu.memoryUtil * 100
        all_gpus_stats.extend([gpu_id,gpu_memorytotal,gpu_memoryUsed,gpu_percent])
    return all_gpus_stats


def cpu_monitor(p):

    cpu_percent = p.cpu_percent()
    mem_percent = p.memory_percent()
    phymem = psutil.virtual_memory()
    phymem_percent=phymem.percent
    phymem_used=int(phymem.used / 1024 / 1024)
    phymem_total=int(phymem.total / 1024 / 1024)
    return [cpu_percent,mem_percent,phymem_percent,phymem_used,phymem_total]



def monitor_system_info(pid):
    current_time = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
    p = psutil.Process(pid)
    all_gpus_stats=gpu_monitor()
    all_cpus_stats=cpu_monitor(p)

    line_cpus =','.join([str(each) for each in all_cpus_stats])
    line_gpus=','.join([str(each) for each in all_gpus_stats])
    line=current_time + ','+line_cpus+','+line_gpus
    print(line)
    f.write(line + "\n")







# from apscheduler.schedulers.background import BackgroundScheduler

def cpu_percent_fun(p):
 cpu_percent = p.cpu_percent()
 print('cpu_percent={}'.format(cpu_percent))
def mem_percent_fun(p):
    mem_percent = p.memory_percent()
    print('mem_percent',mem_percent)
def virtual_mem():
    phymem = psutil.virtual_memory()
    all_mem_percent_str = "Memory: %5s%% %6s/%s" % (
        phymem.percent,
        str(int(phymem.used / 1024 / 1024)) + "M",
        str(int(phymem.total / 1024 / 1024)) + "M"
    )
    print('all_mem_percent_str',all_mem_percent_str)


if __name__=='__main__':
 # # get pid from args
 # if len(sys.argv) < 2:
 #  print("missing pid arg")
 #  sys.exit()
 # # get process
 # pid = int(sys.argv[1])




 pid=32034
 p = psutil.Process(pid)

 cpu_name=['cpu_percent', 'mem_percent', 'phymem_percent', 'phymem_used', 'phymem_total']
 if gpu_amount>1:
     gpu_name=[]
     gpu_name_init = ['gpu_id', 'gpu_memorytotal', 'gpu_memoryUsed', 'gpu_percent']
     for each in range(gpu_amount):
         for name in gpu_name_init:
             gpu_name.append(name+str(each))

 else:
     gpu_name=['gpu_id', 'gpu_memorytotal', 'gpu_memoryUsed', 'gpu_percent']
 f=open("process_monitor_" + p.name() + '_' + str(pid) + ".csv", "a+")

 # [gpu_id, gpu_memorytotal, gpu_memoryUsed, gpu_percent])
 f.write('time,{},{},\n'.format(','.join(cpu_name),','.join(gpu_name)))  # titles
 start_time = time.time()
 scheduler = BlockingScheduler(timezone="Asia/Shanghai")
 # 添加任务,时间间隔5S
 # scheduler.add_job(cpu_percent_fun, 'interval', seconds=2,args=[p])
 # scheduler.add_job(mem_percent_fun, 'interval', seconds=2,args=[p])
 # scheduler.add_job(virtual_mem, 'interval', seconds=2)
 # scheduler.add_job(gpu_monitor,'interval', seconds=2)
 scheduler.add_job(monitor_system_info,'interval', seconds=2,args=[pid])

 # 添加任务,时间间隔2S
 # scheduler.add_job(func, 'interval', seconds=3)
 scheduler.start()

#  try:
#   #  This is here to simulate application activity (which keeps the main thread alive).
#   while True:
#    # time.sleep(1000)
#    if (time.time() - start_time) < 5:
#     pass
#     # print('cost time', time.time() - start_time)
#    else:
#     scheduler.shutdown()
#  except Exception as e:
#   #  Not strictly necessary if daemonic mode is enabled but should be done if possible
#   print('err',e)
# print('end')


