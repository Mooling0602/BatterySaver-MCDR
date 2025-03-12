import threading


config = {}
monitor_task_lock = threading.Lock()
monitor_battery = False
battery_info = {}
check_thread = {}