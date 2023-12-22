#!/usr/bin/env python3
"""
Author: Marcell Barsony
Date  : June 2023
Desc  : Font management tool
"""


import subprocess


class Menu():

    """Docstring for Menu"""

    def __init__(self):
        pass

    @staticmethod
    def display_menu():
        print('[1] Installed (all)')
        print('[2] Installed (monospace)')
        print('[3] Installed (sans-serif)')
        print('[4] Installed (serif)')
        print('[5] Active')

    @staticmethod
    def user_input() -> int:
        while True:
            select = input('> ')
            if select.isdigit() and 1<= int(select) <= 5:
                return int(select)


class FontTools():

    """Docstring for FontTools"""

    @staticmethod
    def get_installed():
        cmd =  'fc-list | grep -ioE ": [^:]*$1[^:]+:" | sed -E "s/(^: |:)//g" | tr , \\n | sort | uniq'
        subprocess.run(cmd, shell=True)

    @staticmethod
    def fc_match(font: str):
        cmd =  f'fc-match {font}'
        out = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, text=True)
        return out.stdout.strip()

    @staticmethod
    def get_fallback(family: str):
        cmd = f'fc-match -a {family}'
        subprocess.run(cmd, shell=True, text=True)

    @staticmethod
    def fc_cache():
        cmd = f'fc-cache -r'
        subprocess.run(cmd, shell=True, text=True)


if __name__ == '__main__':
    m = Menu()
    m.display_menu()
    select = m.user_input()

    f = FontTools()
    if select == 1:
        f.get_installed()
    if select == 2:
        f.get_fallback('monospace')
    if select == 3:
        f.get_fallback('sans-serif')
    if select == 4:
        f.get_fallback('serif')
    if select == 5:
        monospace = f.fc_match('monospace')
        print('Monospace: ', monospace)
        sans_serif = f.fc_match('sans-serif')
        print('Sans-Serif: ', sans_serif)
        sans = f.fc_match('sans')
        print('Serif: ', sans)

    f.fc_cache()
