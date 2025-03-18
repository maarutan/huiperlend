#!/usr/bin/env python3

# changeKeyboard.py
# github: https://github.com/maarutan
# (c) by maaru.tan

import subprocess
import time
import json
import pathlib

# DONE: ####   -----=== global variables ===-----   ####

HOME = pathlib.Path.home()
CURRENT_DIR = pathlib.Path(__file__).parent
ICON_PATH = CURRENT_DIR / ".icons" / "language.svg"
COMMAND = lambda lang: f"notify-send -r 9999 -i {ICON_PATH} '{lang}'"
# COMMAND = lambda lang: f"notify-send -r 9999  '{lang}'"
PADDING = [7, 0]  # padding_left { content } padding_right
NOTIFY = True

# change view content
change_layout_output = {
    "English (US)": "English",
    "Russian": "Russian",
}

# INFO: ####   -----=== logic ===-----   ####


def main():
    changeKeyboard()


def padding_word(icons):
    left_pad, right_pad = PADDING
    return " " * left_pad + icons + " " * right_pad


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
            command, shell=True, text=True, capture_output=True
        ).stdout.strip()


def check_hyprctl() -> bool:
    return bool(shell("command -v hyprctl"))


def changeKeyboard() -> None:
    if not check_hyprctl():
        print("Hyprland not found (hyprctl not available)")
        return

    shell("hyprctl switchxkblayout all next")

    devices_json = shell("hyprctl -j devices")
    if not devices_json:
        print("Failed to get devices information")
        return

    devices = json.loads(devices_json)

    active_keymap = None
    for keyboard in devices.get("keyboards", []):
        if keyboard.get("main", False):
            active_keymap = keyboard.get("active_keymap", None)
            break

    if not active_keymap:
        print("Failed to detect active keyboard layout")
        return

    lang = change_layout_output.get(active_keymap, active_keymap)

    if NOTIFY:
        shell(COMMAND(padding_word(lang)))
    else:
        print(COMMAND(padding_word(lang)))

    time.sleep(0.1)


if __name__ == "__main__":
    main()
