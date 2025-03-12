import battery_saver.data as data
import time

from mcdreforged.api.all import *
from mutils import tr
from . import get_battery_info


@new_thread("BatteryMonitor")
def battery_monitor(server: PluginServerInterface):
    while data.monitor_battery:
        with data.monitor_task_lock:
            bat_p, is_c = get_battery_info(2)
            lev_s = None
            if bat_p:
                if data.battery_info.get("percent", None) is not None:
                    if bat_p > data.battery_info["percent"]:
                        lev_s = "up"
                    if bat_p < data.battery_info["percent"]:
                        lev_s = "down"
                data.battery_info.update(percent=bat_p)
            data.battery_info.update(is_charging=is_c)
            data.battery_info.update(level_shift=lev_s)
            server.dispatch_event(LiteralEvent(f"{server.get_self_metadata().id}:battery_info"), (data.battery_info, ))
            if data.monitor_battery:
                time.sleep(data.config['battery_monitor'].get("monitor_interval", 5))
            else:
                server.logger.warning(tr(server,"task.cancel"))
                break
            if isinstance(data.check_thread, dict) and data.check_thread != {}:
                if data.check_thread.get("src", None) == "console":
                    server.logger.info("Monitor thread running!")
                elif data.check_thread.get("src", None) is not None and isinstance(data.check_thread.get("src", None), str):
                    server.tell(data.check_thread.get("src", None), "Thread BatteryMonitor running!")
                else:
                    server.logger.warning("Reply check source error!")
                data.check_thread = {}