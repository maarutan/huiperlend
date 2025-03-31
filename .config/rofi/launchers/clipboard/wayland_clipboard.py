#!/usr/bin/env python3
# ██████╗  ██████╗ ███████╗██╗
# ██╔══██╗██╔═══██╗██╔════╝██║
# ██████╔╝██║   ██║█████╗  ██║
# ██╔══██╗██║   ██║██╔══╝  ██║
# ██║  ██║╚██████╔╝██║     ██║
# ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝
# ============================
#
#
config = "clipboard"
mode = "-dmenu -display-columns 2"
#
#
#
# =====================
from subprocess import run
import os

dir = os.path.dirname(os.path.realpath(__file__))


# cliphist list | rofi -dmenu | cliphist decode | wl-copy # clipboard
def main():
    shell(f"""cliphist list | rofi \
                 {mode} \
                 -theme {dir}/{config}.rasi  \
                 | cliphist decode | wl-copy
                 """)


def shell(command):
    return run(command, shell=True, capture_output=True, text=True)


if __name__ == "__main__":
    main()
