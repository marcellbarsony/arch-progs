#!/usr/bin/env python3
"""
Author: Marcell Barsony
Date  : June 2023
Desc  : Set up connected X11 displays
"""

import subprocess


def get_displays() -> list:
    displays = []
    result = subprocess.run('xrandr', capture_output=True, text=True)
    for line in result.stdout.splitlines():
        words = line.split()
        if len(words) > 1 and words[1] == "connected":
            display = words[0]
            displays.append(display)
    print('[+] Connected displays ' + str(displays))
    return displays

def display_profiles(displays: list) -> list:
    cmd = []
    for display in displays:
        if display == 'eDP1' or display == 'eDP-1':
            cmd.append(f'xrandr --output {display} --mode 1920x1200 --pos 0x0 --rotate normal')
            if display == 'HDMI1' or display == 'HDMI-1':
                cmd.append(f'xrandr --output {display} --mode 1920x1080 --pos 1920x0 --rotate normal')
            if display == 'DP1' or display == 'DP-1':
                cmd.append(f'xrandr --output {display} --mode 1920x1080 --pos 3840x0 --rotate normal --primary')
        else:
            if display == 'HDMI1' or display == 'HDMI-1':
                cmd.append(f'xrandr --output {display} --mode 1920x1080 --pos 0x0 --rotate normal')
            if display == 'DP1' or display == 'DP-1':
                cmd.append(f'xrandr --output {display} --mode 1920x1080 --pos 1920x0 --rotate normal --primary')
    return cmd

def remove_display(displays: list):
    if len(displays) > 1:
        for display in displays:
            if display == 'eDP1' or display == 'eDP-1':
                subprocess.run(f'xrandr --output {display} --off', shell=True)
                displays.remove(display)
                print(f'[+] Removed: ' + display)
    return displays

def set_displays(cmds: list):
    for cmd in cmds:
        subprocess.run(cmd, shell=True)
        print('[+] Set display: ' + cmd)


if __name__ == "__main__":
    displays = get_displays()
    res = remove_display(displays)
    cmds = display_profiles(res)
    set_displays(cmds)
