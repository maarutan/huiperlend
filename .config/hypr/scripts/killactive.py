#!/usr/bin/env python3
# ----------------------------
# ┬┌─┬┬  ┬  ┌─┐┌─┐┌┬┐┬┬  ┬┌─┐
# ├┴┐││  │  ├─┤│   │ │└┐┌┘├┤
# ┴ ┴┴┴─┘┴─┘┴ ┴└─┘ ┴ ┴ └┘ └─┘
# --------------------------------------------
# (c) maarutan   https://github.com/maarutan

import json
import subprocess


tray_class = [
    "Steam",
]


def get_active_window_class():
    try:
        result = subprocess.run(
            ["hyprctl", "activewindow", "-j"], capture_output=True, text=True
        )
        if result.returncode == 0:
            window_info = json.loads(result.stdout)
            return window_info.get("class", "")
    except Exception as e:
        print(f"Error: {e}")
    return ""


def main():
    window_class = get_active_window_class()
    if window_class in tray_class:
        subprocess.run(["xdotool", "getactivewindow", "windowunmap"])
    else:
        subprocess.run(["hyprctl", "dispatch", "killactive", ""])


if __name__ == "__main__":
    main()
