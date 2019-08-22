import os
import pwd
from datetime import datetime
from socket import gethostname, gethostbyname
from subprocess import check_output
from sys import stdout
from time import sleep

from psutil import disk_usage, sensors_battery, cpu_percent, virtual_memory
from psutil._common import bytes2human
import re


def write(data: str):
    """
    Writes whatever data you'd like it to to stdout
    :param data: Any data as a string
    """
    stdout.write(f'{data}\n')
    stdout.flush()


def fetch_data():
    """
    Fetches data from different sources and formats it to be a nice swaybar line
    """
    name = pwd.getpwuid(os.getuid()).pw_name
    disk_root = bytes2human(disk_usage('/').free)
    disk_home = bytes2human(disk_usage(f'/home/{name}').free)
    try:
        ssid = check_output('nmcli -g CONNECTION,TYPE d | grep wifi', shell=True).strip().decode('utf-8').split(':')[0]
        wireless_info = check_output(f'nmcli -t device wifi | grep {ssid}', shell=True).strip().decode('utf-8')
        bars_in_stars = wireless_info.split(':')[6].count('*')  # e.g. signal is *** out of ****
        current_bars = '▂▄▆█'[0:bars_in_stars]  # Translate stars to bars
        formatted_bars = current_bars + ''.join(['_' for x in range(4 - bars_in_stars)])
    except Exception:
        ip = gethostbyname(gethostname())
        ssid = ip  # Just print the IP instead
        formatted_bars = ''
    battery = int(sensors_battery().percent)
    status = '🔌' if sensors_battery().power_plugged else '🔋'
    date = datetime.now().strftime('%h %d %A %H:%M')
    sound = get_sound()
    cpu = cpu_percent()
    memory = virtual_memory()._asdict()['percent']
    formatted = f'💾: {disk_root}/home/{disk_home} ' \
        f'| CPU: {cpu}% ' \
        f'Mem: {memory}% ' \
        f'| {sound} ' \
        f'| {ssid} {formatted_bars} ' \
        f'| {battery}% {status} ' \
        f'| {date}'
    return formatted


def get_sound():
    output = check_output(['amixer sget Master'], shell=True).strip().decode('utf-8').split('\n')
    volume = 'Unknown'
    for line in output:
        if 'Front Left' in line and 'Playback channels' not in line:
            level = re.search(r'([0-9]{0,3}\%)', line).group(1)
            if 'on' in line:
                volume = f'🔊 {level}'
            if 'off' in line:
                volume = f'🔇 {level}'
    return volume


if __name__ == '__main__':
    """
    Make it run
    """
    while True:
        formatted_text = fetch_data()
        write(formatted_text)
        sleep(1)

# TODO: Split into functions
# TODO: Show ethernet information if connected
