- 中文（简体）
> English not supported yet, use translate tools instead, PRs for this are welcomed!

# BatterySaver-MCDR
简单的服务器电源管理插件，支持自定义配置。

如果觉得好用，请给个Star~

## 用法及注意事项
修改配置，然后插件将按照预期根据主机的电量情况管理服务端的开闭。
> 检测间隔不宜过短或过长，因此推荐使用默认值！

如果你在主机低于设定电量时启动服务器，请确保主机已经连接外部供电，否则服务器仍将在启动完成后自动关闭！

Windows提供的电量精度较低，因此插件可能无法及时获取电量的变化方向，对于普通用户影响不大。

部分设备在特定的操作系统平台上（如小米平板5+Linux）要获取电量信息需要额外的适配工作，若有需要可以发起Issue进行反馈。

## 计划
后面会开发一个定制的扩展插件，基于此插件实现更多功能。
> 包含提前发出提示、接入Im类插件等

该扩展插件短期内不对代码质量和多语言处理方面做任何保证，也暂时没有计划上架到插件仓库，仅会在开发完成后于此说明中进行推荐。
> 咕咕咕！

## 开发
插件会根据配置的检测频次，在每次更新电量信息时派发一个事件，你可以据此开发插件响应这个事件信息实现高度定制化。

要开发MCDReforged插件，请详细阅读此官方[文档](https://docs.mcdreforged.com)

下面是一些代码参考，希望能对你有所帮助：
> 若有误，可以发起Issue反馈，我将尽快修正！
- 插件入口点
```python
from mcdreforged.api.all import *
from your_module.path import on_battery_event

def on_load(server: PluginServerInterface, prev_module):
    pass # 自行处理
    server.register_event_listener("battery_saver:battery_info", on_battery_event)
```
- 响应部分
```python
from needed.module import sth

# 示例
def on_battery_event(server, battery_info: dict):
    server.logger.info(f"电量（百分比）：{battery_info.get('percent', None)}")
    server.logger.info(f"外部供电（布尔值）：{battery_info.get('is_charging', None)}")
    server.logger.info(f"变化方向（字符串）：{battery_info.get('level_shift', None)}")
    if battery_info.get('is_charging', None) is True:
        server.logger.info("主机充电中……")
    if battery_info.get('level_shift', None) == "up":
        server.logger.info("电量正在增加！")
    if battery_info.get('level_shift', None) == "down":
        server.logger.info("电量正在减少！")
    pass # 自行处理
```
- 插件元数据`mcdreforged.plugin.json`
> 仅包括需修改的部分，其他部分自行处理
```json
{
	"dependencies": {
		"mcdreforged": ">=2.1.0",
		"battery_saver": ">=0.1.0"
	}
}
```