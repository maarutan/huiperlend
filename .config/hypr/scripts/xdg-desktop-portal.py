#!/usr/bin/env python3
# ─┐ ┬┌┬┐┌─┐  ┌─┐┌─┐┬─┐┌┬┐┌─┐┬
# ┌┴┬┘ │││ ┬  ├─┘│ │├┬┘ │ ├─┤│
# ┴ └──┴┘└─┘  ┴  └─┘┴└─ ┴ ┴ ┴┴─┘
# --------------------------------------------
# (c) maarutan   https://github.com/maarutan

import subprocess
from time import sleep


def killall_xdg_desktop_portal():
    subprocess.run(["killall", "-e", "xdg-desktop-portal-hyprland"])
    sleep(1)
    subprocess.run(["killall", "-e", "xdg-desktop-portal-wlr"])
    subprocess.run(["killall", "-e", "xdg-desktop-portal"])
    subprocess.Popen(["killall", "-e", "/usr/lib/xdg-desktop-portal-hyprland"])
    sleep(2)
    subprocess.Popen(["killall", "-e", "/usr/lib/xdg-desktop-portal"])


if __name__ == "__main__":
    killall_xdg_desktop_portal()
