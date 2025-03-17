#!/usr/bin/env python3

# vi-mode.py
# github: https://github.com/maarutan
# (c) by maaru.tan

import os
import argparse
import subprocess

# DONE: ----=== Global variables ===----

TML_FILE = "/tmp/vi-mode"
NOCAPS = True


# INFO: ---=== logic ===---


def enable_vi_mode():
    keymap = [
        ("43", "Left"),
        ("44", "Down"),
        ("45", "Up"),
        ("46", "Right"),
    ]

    for keycode, direction in keymap:
        subprocess.run(
            [
                "xmodmap",
                "-e",
                f"keycode {keycode} = {direction} NoSymbol {direction} NoSymbol",
            ]
        )

    open(TML_FILE, "w").close()
    subprocess.run(["notify-send", "Vi Mode ON"])


def disable_vi_mode():
    if NOCAPS:
        subprocess.run(["setxkbmap", "-option", "ctrl:nocaps"])
    else:
        subprocess.run(["setxkbmap", "-option", ""])

    if os.path.exists(TML_FILE):
        os.remove(TML_FILE)

    subprocess.run(["notify-send", "Vi Mode OFF"])


def toggle_vi_mode():
    if os.path.exists(TML_FILE):
        disable_vi_mode()
    else:
        enable_vi_mode()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Toggle Vi Mode for keyboard navigation (HJKL -> Arrow Keys)"
    )
    parser.add_argument("-e", "--enable", action="store_true", help="Enable Vi Mode")
    parser.add_argument("-d", "--disable", action="store_true", help="Disable Vi Mode")

    args = parser.parse_args()

    if args.enable:
        enable_vi_mode()
    elif args.disable:
        disable_vi_mode()
    else:
        toggle_vi_mode()
