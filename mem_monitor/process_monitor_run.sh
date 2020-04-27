res=$(ps -ef |grep 'waitress-serve --listen=\*:8888' |awk '{print $2}')
python3 process_monitor_new.py $res
