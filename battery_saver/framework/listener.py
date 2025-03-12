import battery_saver.data as data

from mcdreforged.api.all import *


def on_battery_event(server: PluginServerInterface, battery_info: dict):
    server.logger.debug(f"Is charging: {battery_info.get('is_charging', None)}")
    server.logger.debug(f"Battery percent: {battery_info.get('percent', None)}")
    server.logger.debug(f"Level shift: {battery_info.get('level_shift', None)}")
    if battery_info.get("level_shift", None) == "down"\
        and battery_info.get("percent", None) < data.config['battery_monitor'].get('low_battery_threshold', 30)\
        and battery_info.get("is_charging", None) is False:
        if data.stop_server_when_lowb is True:
            server.stop()
            data.stop_server_when_lowb = False
    if battery_info.get("percent", None) >= data.config['battery_monitor'].get('enough_battery_to_start', 50):
        if not server.is_server_running():
            server.start()
            data.stop_server_when_lowb = True