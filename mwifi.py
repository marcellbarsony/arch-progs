#!/usr/bin/env python3
"""
Author: Name
Date  : 05/13/23
Desc  : Wi-Fi setup tool
"""


import getpass
import subprocess


def user_input() -> tuple:
    wifi_ssid = input('Wi-Fi SSID: ')
    wifi_pass = getpass.getpass('Wi-Fi Pass: ')
    return str(wifi_ssid), str(wifi_pass)


def wifi_connect(credentials: tuple):
    cmd = f'nmcli device wifi connect {credentials[0]} password {credentials[1]}'
    try:
        subprocess.run(cmd, shell=True, check=True)
    except Exception as err:
        print(err)


if __name__ == "__main__":
    credentials = user_input()
    wifi_connect(credentials)
