#!/usr/bin/env python3

# check_notify.py
# github: https://github.com/maarutan
# (c) by maaru.tan


import subprocess
import sys
import os

# Global variables
TMP_FILE = "/tmp/touchpad_tmp_config"
user = os.environ["USER"]


def shell(command: list[str]) -> str | None:
    blacklist = {"/sbin/poweroff", "/sbin/reboot", "/bin/rm", "/sbin/shutdown"}

    if command[0] in blacklist:
        print(f"Skipping dangerous command: {' '.join(command)}")
        return None

    try:
        return subprocess.check_output(command, text=True).strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None


def notify_send(message: str = "", WARN: bool = False, INFO: bool = False):
    icon = (
        "dialog-warning" if WARN else "dialog-information" if INFO else "dialog-message"
    )
    subprocess.run(["notify-send", "--icon", icon, message])


if __name__ == "__main__":
    notify_send(f" ---=== Hello {user} ===---", INFO=False, WARN=False)
