import psutil
import time
from mcdreforged.api.all import *

CHECK_INTERVAL = 5
SHUTDOWN_THRESHOLD = 30
psi = ServerInterface.psi()
stop_check = False

def empty():
    pass

def get_battery_info() -> str:
    battery = psutil.sensors_battery()
    if battery:
        return f"Battery percentage: {battery.percent}%, Power plugged in: {'Yes' if battery.power_plugged else 'No'}"
    else:
        return "Battery information not available."

def check_battery_status():
    battery = psutil.sensors_battery()
    if battery is not None:
        if battery.percent < SHUTDOWN_THRESHOLD and not battery.power_plugged:
            psi.broadcast(f"[BatterySaver] Battery is below {SHUTDOWN_THRESHOLD}%. Shutting down server.")
            psi.stop()
            psi.exit()
        else:
            empty()
    else:
        psi.logger.warning("Battery information not available.")

def on_load(server: PluginServerInterface, old):
    server.logger.info("Plugin BatterySaver enabled.")
    server.logger.info("Starting battery monitoring task")
    server.register_command(
        Literal('!!battery')
        .runs(
            lambda src: src.reply(get_battery_info())
        )
    )
    main()

def unload():
    global stop_check
    stop_check = True

@new_thread
def main():    
    while True:
        check_battery_status()
        if stop_check:
            break
        time.sleep(CHECK_INTERVAL)

def on_unload(server: PluginServerInterface):
    unload()
    time.sleep(CHECK_INTERVAL + 1)
    server.logger.info("BatterySaver unloaded.")