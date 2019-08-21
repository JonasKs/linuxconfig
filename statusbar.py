from datetime import datetime
from socket import gethostname, gethostbyname
from subprocess import check_output
from sys import stdout
from time import sleep
import pwd
import os

from psutil import disk_usage, sensors_battery
from psutil._common import bytes2human


def write(data: str):
    """
    Writes whatever data you'd like it to to stdout
    :param data: Any data as a string
    """
    stdout.write(f'{data}\n')
    stdout.flush()


def fetch_data():
    name = pwd.getpwuid( os.getuid() ).pw_name
    disk_root = bytes2human(disk_usage('/').free)
    disk_home = bytes2human(disk_usage(f'/home/{name}').free)
    # ip = gethostbyname(gethostname()) # Unused for now
    try:
        ssid = check_output('nmcli -g CONNECTION,TYPE d | grep wifi', shell=True).strip().decode('utf-8').split(':')[0]
        wireless_info = check_output(f'nmcli -t device wifi | grep {ssid}', shell=True).strip().decode('utf-8')
        wireless_as_list = wireless_info.split(':')
        bars_in_stars = wireless_as_list[6].count('*')
        if bars_in_stars == 4:
            bars = '▂▄▆█'
        elif bars_in_stars == 3:
            bars = '▂▄▆_'
        elif bars_in_stars == 2:
            bars = '▂▄__'
        elif bars_in_stars == 1:
            bars = '▂___'
        else:
            bars = '____'
    except Exception:
        ssid = ''
        bars = ''
    battery = int(sensors_battery().percent)
    status = 'Charging' if sensors_battery().power_plugged else 'Discharging'
    date = datetime.now().strftime('%h %d %A %H:%M')
    formatted = f'💾: {disk_root}/home/{disk_home} | {ssid} {bars} | 🔋: {battery}% {status} | {date}'
    return formatted


while True:
    formatted_text = fetch_data()
    write(formatted_text)
    sleep(1)
