import os
import psutil
import time

from mcdreforged.api.all import *
from mutils import extract_file


psi = ServerInterface.psi()
stop_check = False

def get_battery_info() -> str:
    try:
        battery = psutil.sensors_battery()
        if battery:
            return f"电池电量: {battery.percent}%, 外部电源: {'已连接' if battery.power_plugged else '未连接'}"
        else:
            return "无法获取电池信息。"
    except Exception as e:
        return f"获取电池信息出错: {e}"

def check_battery_status():
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            psi.logger.warning("无法获取电池信息。")
            return
        if battery.percent < SHUTDOWN_THRESHOLD and not battery.power_plugged:
            msg = f"[BatterySaver] 电池电量低于 {SHUTDOWN_THRESHOLD}% 且未插电，正在关闭服务器。"
            psi.broadcast(msg)
            psi.stop()
    except Exception as e:
        psi.logger.error(f"检查电池状态时出错: {e}")

@new_thread("BatteryMonitor")
def battery_monitor():
    while not stop_check:
        check_battery_status()
        time.sleep(CHECK_INTERVAL)

def on_load(server: PluginServerInterface, old):
    global SHUTDOWN_THRESHOLD, CHECK_INTERVAL, MONITOR_ENABLED
    # 解压配置文件（确保带有注释）
    config_file = os.path.join(server.get_data_folder(), 'config.yml')
    if not os.path.exists(config_file):
        extract_file(server, os.path.join('resources', 'config.yml'), config_file)
    # 加载配置文件
    config_version = str(server.get_self_metadata().version)
    server.logger.info(f"当前配置文件版本：{config_version}")
    config = server.load_config_simple('config.yml', default_config={
        'battery_monitor': {
            'low_battery_threshold': 30,
            'check_interval': 5,
            'enabled': True,
            'version': config_version
        }
    })

    SHUTDOWN_THRESHOLD = config['battery_monitor']['low_battery_threshold']
    CHECK_INTERVAL = config['battery_monitor']['check_interval']
    MONITOR_ENABLED = config['battery_monitor']['enabled']
    CONFIG_VERSION = config['battery_monitor'].get('version', None)

    if CONFIG_VERSION != config_version:
        if not os.path.exists(f"{config_file}.bak"):
            os.rename(config_file, f"{config_file}.bak")
        else:
            os.remove(f"{config_file}.bak")
            os.rename(config_file, f"{config_file}.bak")
        server.logger.warning("配置文件版本不匹配，已备份上一版本旧配置文件，请及时根据备份内容修改配置！")
        server.reload_plugin(server.get_self_metadata().id)

    server.logger.info(f"电池监控任务将在服务器启动完成后启动，检查间隔为 {CHECK_INTERVAL} 秒。")
    # 注册显示电池状态的指令
    server.register_command(
        Literal('!!battery')
        .runs(lambda src: src.reply(get_battery_info()))
    )

    if server.is_server_startup():
        on_server_startup(server)

def on_server_startup(server: PluginServerInterface):
    if MONITOR_ENABLED:
        battery_monitor()
    else:
        server.logger.info("电池监控功能未启用。")

def clean_task():
    global stop_check
    stop_check = True

def on_unload(server: PluginServerInterface):
    clean_task()
    # 等待足够时间确保后台线程能够结束
    time.sleep(CHECK_INTERVAL + 1)
    server.logger.info("BatterySaver 插件已卸载。")