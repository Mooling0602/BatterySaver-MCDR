import battery_saver.data as data

from mcdreforged.api.all import *
from mutils import execute_if
from .config import *
from .listener import on_battery_event
from battery_saver.core.task import battery_monitor
from battery_saver.core import get_battery_info


builder = SimpleCommandBuilder()

def on_load(server: PluginServerInterface, old):
    load_config(server)
    if check_config is not None:
        check_config(server)
    builder.register(server)
    if server.is_server_startup():
        on_server_startup(server)
    if not server.is_server_running():
        data.stop_server_when_lowb = False
    server.register_event_listener(f"{server.get_self_metadata().id}:battery_info", on_battery_event)

@execute_if(lambda: data.config['battery_monitor'].get("enabled", None))
def on_server_startup(server: PluginServerInterface):
    data.monitor_battery = True
    server.logger.info(tr(server, "task.start"))
    battery_monitor(server)
    server.logger.info(f"Thread status: {data.monitor_battery}")

def on_unload(server: PluginServerInterface):
    server.logger.info("Cleaning plugin thread...")
    data.monitor_battery = False

@builder.command('!!battery')
def on_query(src: CommandSource):
    bat_p, is_c = get_battery_info(2)
    src.reply(data.config['battery_monitor'].get('reply_format', None).format(bat_p=bat_p, is_c=is_c))

@builder.command('!!battery status')
def on_status(src: CommandSource):
    if src.is_console:
        data.check_thread = {"src": "console"}
    else:
        data.check_thread = {"src": f"{src.player}"}