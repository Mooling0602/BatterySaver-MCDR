import battery_saver.data as data
import os

from mcdreforged.api.all import *
from mutils import extract_file, execute_if, tr

config_ver = '0.1.0'


def load_config(server: PluginServerInterface):
    config_path = os.path.join(server.get_data_folder(), 'config.yml')
    if not os.path.exists(config_path):
        if server.get_mcdr_language() == 'zh_cn':
            config_resource_path = os.path.join('resources', 'config.default.zh.yml')
        else:
            config_resource_path = os.path.join('resources', 'config.default.yml')
        extract_file(server, config_resource_path, config_path)
    server.logger.info(server.rtr(f"{server.get_self_metadata().id}.plugin.current_ver", config_ver=config_ver))
    data.config = server.load_config_simple(file_name='config.yml', default_config={
        'battery_monitor': {
            'enough_battery_to_start': 50,
            'low_battery_threshold': 30,
            'check_interval': 5,
            'enabled': True,
            'reply_format': 'Battery: {bat_p}%, is charging: {is_c}',
            'version': config_ver
        }
    }, echo_in_console=False)
    server.logger.info(tr("config.loaded"))

@execute_if(lambda: data.config != {} and data.config is not None)
def check_config(server: PluginServerInterface):
    config_path = os.path.join(server.get_data_folder(), 'config.yml')
    prev_config_ver = data.config['battery_monitor'].get('version', None)
    if prev_config_ver != config_ver:
        server.logger.warning(tr("config.mismatch"))
        if not os.path.exists(f"{config_path}.bak"):
            os.rename(config_path, f"{config_path}.bak")
        else:
            server.logger.warning(tr("config.remove_bak"))
            os.remove(f"{config_path}.bak")
            os.rename(config_path, f"{config_path}.bak")
        server.reload_plugin(server.get_self_metadata().id)
    else:
        server.logger.info(tr("config.check_passed"))