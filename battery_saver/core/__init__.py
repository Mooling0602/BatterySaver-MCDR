import psutil

from typing import Optional


def get_battery_info(decimal_place: Optional[int] = None) -> tuple:
    battery_data = psutil.sensors_battery()
    battery = round(battery_data.percent, decimal_place)\
        if decimal_place is not None else battery_data.percent
    is_charging = battery_data.power_plugged
    return battery, is_charging

