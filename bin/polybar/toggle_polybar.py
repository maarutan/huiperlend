#!/usr/bin/env python3

import subprocess
import time, pathlib


def is_polybar_running():
    result = subprocess.run(["pgrep", "-x", "polybar"], capture_output=True)
    return result.returncode == 0


def toggle_polybar():
    if is_polybar_running():
        subprocess.run(["killall", "-q", "polybar"])
        time.sleep(1)
        subprocess.run(["bspc", "config", "-m", "focused", "top_padding", "0"])
    else:
        subprocess.run([pathlib.Path(__file__).parent / "runner.py"], shell=True)
        subprocess.run(["bspc", "config", "-m", "focused", "top_padding", "31"])


if __name__ == "__main__":
    try:
        toggle_polybar()
    except:
        print("\n cancel")
