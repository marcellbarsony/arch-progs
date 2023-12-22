#!/usr/bin/env python3
"""
Author: Marcell Barsony
Date  : June 2023
Desc  : Xwallpaper tools
TODO  : - Exclude Mobile & Windows
        - Wallpaper history
"""


import argparse
import os
import random
import shutil
import subprocess
import urllib.request
import zipfile


user = os.getlogin()
path = f"/home/{user}/Downloads/Backgrounds"


class Display():

    """Docstring for Displays"""

    @staticmethod
    def get_displays() -> list:
        result = subprocess.run("xrandr", capture_output=True, text=True)
        displays = []
        for line in result.stdout.splitlines():
            words = line.split()
            if len(words) > 1 and words[1] == "connected":
                display_name = words[0]
                displays.append(display_name)
        return displays

    @staticmethod
    def remove_display(displays: list):
        if len(displays) > 1:
            for display in displays:
                if display == "eDP1" or display == "eDP-1":
                    subprocess.run(f"xrandr --output {display} --off", shell=True)
                    displays.remove(display)
        return displays


class Wallpaper():

    """Docstring for Wallpaper"""

    @staticmethod
    def get_files(path: str) -> list:
        files = []
        for root, _, filenames in os.walk(path):
            if "mobile" in root or "windows" in root:
                continue
            for filename in filenames:
                files.append(os.path.join(root, filename))
        return files

    @staticmethod
    def get_random(files: list) -> str:
        file = random.choice(files)
        return file

    @staticmethod
    def set_wallpaper(displays: list, file: str):
        for display in displays:
            cmd = f"xwallpaper --output {display} --stretch {file}"
            subprocess.run(cmd, shell=True)


class Update():

    """Docstring for Update"""

    def __init__(self, path: str):
        self.path = path
        self.url = "https://www.dropbox.com/scl/fo/5loqjisrohzslojb5ibmw/h?rlkey=onmox6lkop8uf9wzd314pbj66&dl=1"
        self.out = f"{self.path}/wallpapers.zip"

    def directory(self):
        if os.path.exists(self.path):
            shutil.rmtree(self.path, ignore_errors=True)
            print("[+] Removing wallpapers")
            os.mkdir(self.path)
            print("[+] Creating directory")
        else:
            os.mkdir(self.path)
            print("[+] Creating directory")

    def download(self):
        print("[I] Downloading...")
        urllib.request.urlretrieve(self.url, self.out)

    def unzip(self):
        with zipfile.ZipFile(self.out, "r") as zip_ref:
            zip_ref.extractall(self.path)
        print("[+] Unzipping")
        os.remove(self.out)
        print("[+] Removing zip")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="xwall.py",
        description="X11 wallpaper setup",
        epilog="TODO"
    )

    parser.add_argument("-r", "--random", action="store_true", help="Random wallapper")
    parser.add_argument("-u", "--update", action="store_true", help="Update wallpapers")

    args = parser.parse_args()

    if args.random:
        m = Display()
        displays_active = m.get_displays()
        displays = m.remove_display(displays_active)
        w = Wallpaper()
        files = w.get_files(path)
        file = w.get_random(files)
        w.set_wallpaper(displays, file)
        print("[+] Random wallpaper " + str(displays))

    if args.update:
        u = Update(path)
        u.directory()
        u.download()
        u.unzip()
