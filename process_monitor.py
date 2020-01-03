import sys
import time
import psutil

# get pid from args
if len(sys.argv) < 2:
	print ("missing pid arg")
	sys.exit()

# get process
pid = int(sys.argv[1])
p = psutil.Process(pid)

# monitor process and write data to file
interval = 3 # polling seconds
with open("process_monitor_" + p.name() + '_' + str(pid) + ".csv", "a+") as f:
	f.write("time,cpu%,mem%,all_cpu%,all_mem%\n") # titles
	while True:
		current_time = time.strftime('%Y%m%d-%H%M%S',time.localtime(time.time()))
		cpu_percent = p.cpu_percent()
		all_cpu_percent=psutil.cpu_percent()
		mem_percent = p.memory_percent()

		phymem = psutil.virtual_memory()
		all_mem_percent_str = "Memory: %5s%% %6s/%s" % (
			phymem.percent,
			str(int(phymem.used / 1024 / 1024)) + "M",
			str(int(phymem.total / 1024 / 1024)) + "M"
		)



		line = current_time + ',' + str(cpu_percent) + ',' + str(mem_percent)+ ',' +str(all_cpu_percent)+ ',' +all_mem_percent_str
		print (line)
		f.write(line + "\n")
		time.sleep(interval)
