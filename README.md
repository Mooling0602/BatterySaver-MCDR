# BatterySaver
简单的服务器电源管理插件，支持自定义配置。

## 用法
修改配置中的检测频次和最低关服电量，然后插件将在服务器启动完成后达到最低关服电量时自动关服。

目前不支持在开服时服务器电量已低于设定值时取消自动关服任务或阻断服务器启动，因此如果你这样做体验会很不好（服务器开启完毕后立即被关闭）。
