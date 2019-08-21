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
    name = pwd.getpwuid(os.getuid()).pw_name
    disk_root = bytes2human(disk_usage('/').free)
    disk_home = bytes2human(disk_usage(f'/home/{name}').free)
    # ip = gethostbyname(gethostname()) # Unused for now
    try:
        ssid = check_output('nmcli -g CONNECTION,TYPE d | grep wifi', shell=True).strip().decode('utf-8').split(':')[0]
        wireless_info = check_output(f'nmcli -t device wifi | grep {ssid}', shell=True).strip().decode('utf-8')
        bars_in_stars = wireless_info.split(':')[6].count('*')  # e.g. signal is *** out of ****
        bars = '▂▄▆█'  # Just prettier formatting
        current_bars = bars[0:bars_in_stars]  # Translate stars to bars
        formatted_bars = current_bars + ''.join(['_' for x in range(4 - bars_in_stars)])
    except Exception:
        ssid = ''
        formatted_bars = ''
    battery = int(sensors_battery().percent)
    status = 'Charging' if sensors_battery().power_plugged else 'Discharging'
    date = datetime.now().strftime('%h %d %A %H:%M')
    formatted = f'💾: {disk_root}/home/{disk_home} | {ssid} {formatted_bars} | 🔋: {battery}% {status} | {date}'
    return formatted


while True:
    formatted_text = fetch_data()
    write(formatted_text)
    sleep(1)
