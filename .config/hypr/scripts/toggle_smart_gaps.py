#!/usr/bin/env python3
# ┌┬┐┌─┐┌─┐┌─┐┬  ┌─┐  ┌─┐┌┬┐┌─┐┬─┐┌┬┐  ┌─┐┌─┐┌─┐┌─┐
#  │ │ ││ ┬│ ┬│  ├┤   └─┐│││├─┤├┬┘ │   │ ┬├─┤├─┘└─┐
#  ┴ └─┘└─┘└─┘┴─┘└─┘  └─┘┴ ┴┴ ┴┴└─ ┴   └─┘┴ ┴┴  └─┘
# --------------------------------------------
# (c) maarutan   https://github.com/maarutan

import subprocess
import json
import sys


def get_workspace_id() -> int:
    id = subprocess.run(
        ["hyprctl", "activeworkspace", "-j"], capture_output=True, text=True
    ).stdout
    id = json.loads(id)
    return id["id"]


def get_active_window_id() -> int:
    rid = subprocess.run(
        ["hyprctl", "activewindow", "-j"], capture_output=True, text=True
    ).stdout
    rid = json.loads(rid)
    return rid["id"]


def get_current_in_gaps() -> int:
    gaps = subprocess.run(
        ["hyprctl", "workspacerules", "-j"], capture_output=True, text=True
    ).stdout
    gaps = json.loads(gaps)
    print(f"Current in gaps: {gaps}")  # Отладка
    return gaps[0]["gapsIn"][0] if gaps else 0


def get_current_out_gaps() -> int:
    gaps = subprocess.run(
        ["hyprctl", "workspacerules", "-j"], capture_output=True, text=True
    ).stdout
    gaps = json.loads(gaps)
    print(f"Current out gaps: {gaps}")  # Отладка
    return gaps[0]["gapsOut"][0] if gaps else 0


def run_subprocess(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing command: {' '.join(command)}")
        print(f"Error details: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if get_current_in_gaps() == 0 and get_current_out_gaps() == 0:
        run_subprocess(
            [
                "hyprctl",
                "keyword",
                "workspace",
                f"{get_active_window_id()} f[1]",
                "gapsin:0",
                "gapsout:0",
            ]
        )
        run_subprocess(
            [
                "hyprctl",
                "keyword",
                "workspace",
                f"{get_active_window_id()} w[tv1]",
                "gapsin:0",
                "gapsout:0",
            ]
        )
        sys.exit(0)

    run_subprocess(["hyprctl", "reload"])
