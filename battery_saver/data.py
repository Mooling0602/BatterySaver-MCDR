import threading


config = {}
monitor_task_lock = threading.Lock()
monitor_battery = False
stop_server_when_lowb = True
battery_info = {}
check_thread = {}
