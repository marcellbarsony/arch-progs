#!/usr/bin/env python3
"""
Author: Marcell Barsony
Date  : May 2023
Desc  : Update Pacman mirrorlist
"""


import subprocess


def mirrorlist():
    cmd = "sudo \
    reflector \
    --latest 25 \
    --protocol https \
    --connection-timeout 5 \
    --sort rate \
    --save /etc/pacman.d/mirrorlist"
    try:
        print("Updating Pacman mirrorlist...")
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL)
        print("[+] PACMAN: Mirrorlist")
    except subprocess.CalledProcessError as err:
        print(f"[-] PACMAN: Mirrorlist {err}")


if __name__ == "__main__":
    mirrorlist()
