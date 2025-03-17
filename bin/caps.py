#!/usr/bin/env python3

# toggle_touchpad.py
# github: https://github.com/maarutan
# (c) by maaru.tan

import subprocess
import sys
import os

# Global variables
TMP_FILE = "/tmp/touchpad_tmp_config"
user = os.environ["USER"]


def main():
    shell("setxkbmap -option 'ctrl:nocaps'")
    notify_send(
        " ---=== Capslock ===--- \n[caps in ctrl] changed 😃",
        TIMEOUT=2000,
    )


def shell(command) -> str | None:
    blacklist = [
        "poweroff",
        "reboot",
        "rm",
        "shutdown",
    ]
    if command.split()[0] in blacklist:
        return print(f"skipping: {command}")
    else:
        return subprocess.run(
            command,
            shell=True,
            text=True,
            capture_output=True,
        ).stdout.strip()


def notify_send(
    message: str = "",
    WARN: bool = False,
    INFO: bool = False,
    ICON: str = "",
    TIMEOUT: int = 1000,
    NOTIFY_ID: int = 0,
):
    icon = (
        (
            "dialog-warning"
            if WARN
            else "dialog-information"
            if INFO
            else "dialog-message"
        )
        if ICON == ""
        else ICON
    )

    subprocess.run(
        [
            "notify-send",
            "-t",
            str(TIMEOUT),
            "-r",
            str(NOTIFY_ID),
            "--icon",
            icon,
            message,
        ]
    )


if __name__ == "__main__":
    main()
