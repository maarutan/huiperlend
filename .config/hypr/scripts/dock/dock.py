#!/usr/bin/env python3
#
# ┌┬┐┌─┐┌─┐┬┌─  ┬ ┬┬ ┬┌─┐┬─┐┬  ┌─┐┌┐┌┌┬┐
#  │││ ││  ├┴┐  ├─┤└┬┘├─┘├┬┘│  ├─┤│││ ││
# ─┴┘└─┘└─┘┴ ┴  ┴ ┴ ┴ ┴  ┴└─┴─┘┴ ┴┘└┘─┴┘
# --------------------------------------------
# (c) maarutan   https://github.com/maarutan


import os
import time
import json
import subprocess
import socket
import argparse
import shutil
import pathlib
import sys


# INFO:-------=== Global Variables ===-------


DEBUG = False
DOCK_TYPE = "intelectual"  # "push", "always", "nothower" or "intelectual"
LAUNCH_UP = True
LAUNCHERS = "rofi -show drun"
LAUNCHERS_POS = "left"  # "left" or "right"
FULL_DOCK = False  # (default False )
POSITION_DOCK = "bottom"  # "left" "right" "center" "bottom" (default "center")
ALIMENT_DOCK = "center"  # "start", "center" or "end" (default "center")
HEIGHT_DOCK = 30
ICON_SIZE = 48
MARGIN_DOCK = [0, 00, 10, 00]  # [left, top, bottom, right] (default [0, 0, 0, 0])
LAUNCHERS_ICON = (
    pathlib.Path.home()
    / ".config"
    / "hypr"
    / "scripts"
    / "dock"
    / ".icon"
    / "grid_dark.svg"
)


# DONE:-------=== Functions ===-------


def main():
    try:
        if dynamic():
            if DOCK_TYPE == "intelectual":
                start_dock("-d")
            elif DOCK_TYPE == "nothower":
                start_dock("-r")
            listen_for_events()
        else:
            if DOCK_TYPE == "push":
                start_dock("-x")
            if DOCK_TYPE == "always":
                start_dock("-r", UPDATE_DOCK=False)
            listen_for_events_for_not_dynamic()
    except KeyboardInterrupt:
        print("\n\nbye bye !!!")


TOGGLE_SIGNAL = "pkill -35 -f nwg-dock-hyprland"
SHOW_SIGNAL = "pkill -36 -f nwg-dock-hyprland"
HIDE_SIGNAL = "pkill -37 -f nwg-dock-hyprland"


def toggle_dock(action):
    signal = SHOW_SIGNAL if action == "show" else HIDE_SIGNAL
    os.system(signal)


def get_active_ws_id(monitor_info):
    lines = monitor_info.split("\n")
    ws_id = lines[1]
    special_ws_id = lines[2]
    return special_ws_id if special_ws_id != "0" else ws_id


def dynamic() -> bool:
    if DOCK_TYPE == "intelectual" or DOCK_TYPE == "nothower":
        return True
    else:
        return False


def get_fullscreen_state():
    result = subprocess.run(
        ["hyprctl", "activewindow", "-j"], capture_output=True, text=True
    ).stdout
    fullscreen_info = json.loads(result)
    return bool(fullscreen_info.get("fullscreen"))


def handle(event):
    if DEBUG:
        print(f"Handling event: {event}")
    if event.startswith("fullscreen>>"):
        fullscreen_state = event.split(">>")[1]
        if fullscreen_state.isdigit():
            fullscreen_state = int(fullscreen_state)
            if fullscreen_state > 0:
                if DEBUG:
                    print("Fullscreen detected, hiding dock.")
                toggle_dock("hide")
            else:
                if DEBUG:
                    print("Exiting fullscreen, showing dock.")
                show_hide_dock()
    else:
        if any(
            event.startswith(prefix)
            for prefix in [
                "changefloatingmode",
                "workspacev2",
                "closewindow",
                "openwindow",
                "activespecial",
            ]
        ):
            show_hide_dock()
        elif event.startswith("focusedmon"):
            show_hide_dock()
            toggle_dock("hide")


def handle_for_not_dynamic(event):
    if DEBUG:
        print(f"Handling event: {event}")
    if event.startswith("fullscreen>>"):
        fullscreen_state = event.split(">>")[1]
        if fullscreen_state.isdigit():
            fullscreen_state = int(fullscreen_state)
            if fullscreen_state > 0:
                if DEBUG:
                    print("Fullscreen detected, hiding dock.")
                toggle_dock("hide")
            else:
                if DEBUG:
                    print("Exiting fullscreen, showing dock.")
                toggle_dock("show")
    else:
        if any(
            event.startswith(prefix)
            for prefix in [
                "changefloatingmode",
                "workspacev2",
                "closewindow",
                "openwindow",
                "activespecial",
            ]
        ):
            # show_hide_dock()
            toggle_dock("show")
        elif event.startswith("focusedmon"):
            # show_hide_dock()
            toggle_dock("show")


def show_hide_dock():
    if get_fullscreen_state():
        if DEBUG:
            print("Fullscreen detected, hiding dock.")
        toggle_dock("hide")
        return

    monitor_info = subprocess.run(
        ["hyprctl", "monitors", "-j"], capture_output=True, text=True
    ).stdout
    monitors = json.loads(monitor_info)
    focused_monitor = next((m for m in monitors if m["focused"]), None)

    if not focused_monitor:
        return

    monitor_height = focused_monitor["height"]
    ws_id = get_active_ws_id(
        f"{monitor_height}\n{focused_monitor['activeWorkspace']['id']}\n{focused_monitor['specialWorkspace']['id']}"
    )

    workspaces = json.loads(
        subprocess.run(
            ["hyprctl", "workspaces", "-j"], capture_output=True, text=True
        ).stdout
    )

    window_count = next((w["windows"] for w in workspaces if w["id"] == int(ws_id)), 0)

    if window_count == 0:
        toggle_dock("show")
        return

    windows_data = json.loads(
        subprocess.run(
            ["hyprctl", "clients", "-j"], capture_output=True, text=True
        ).stdout.strip()
    )

    if window_count == 0 or windows_data == "[]":
        toggle_dock("show")
        return

    should_show = True

    for window in windows_data:
        if window["workspace"]["id"] == int(ws_id):
            pos_y = window["at"][1]
            size_y = window["size"][1]
            free_space = monitor_height - pos_y - size_y

            if free_space < HEIGHT_DOCK:
                should_show = False
                break

    toggle_dock("show" if should_show else "hide")


def start_dock(TYPE_DOCK: str, UPDATE_DOCK: bool = True):
    try:
        args = [
            "nwg-dock-hyprland",
            TYPE_DOCK,
            "-i",
            str(ICON_SIZE),
            "-a",
            ALIMENT_DOCK,
            "-p",
            POSITION_DOCK,
            "-mb",
            str(MARGIN_DOCK[2]),
            "-mr",
            str(MARGIN_DOCK[3]),
            "-ml",
            str(MARGIN_DOCK[0]),
            "-mt",
            str(MARGIN_DOCK[1]),
        ]

        if FULL_DOCK:
            args.append("-f")
        if LAUNCH_UP:
            if LAUNCHERS_POS == "left":
                args.extend(["-c", str(LAUNCHERS), "-lp", "start"])
            elif LAUNCHERS_POS == "right":
                args.extend(["-c", str(LAUNCHERS), "-lp", "end"])

        args.extend(["-ico", str(LAUNCHERS_ICON)])
        args.extend(["2>/dev/null"])

        time.sleep(0.6)
        if UPDATE_DOCK:
            show_hide_dock()
            subprocess.Popen(args)
        else:
            subprocess.run(args)
            sys.exit(0)

    except Exception as e:
        print(f"Error in start_dock: {e}")


def listen_for_events():
    try:
        socket_path = os.path.join(
            os.environ.get("XDG_RUNTIME_DIR", "/run/user/1000"),
            f"hypr/{os.environ.get('HYPRLAND_INSTANCE_SIGNATURE', '')}/.socket2.sock",
        )
        if DEBUG:
            print(f"Connecting to socket at {socket_path}")

        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.connect(socket_path)
            with client.makefile("r") as stream:
                for line in stream:
                    handle(line.strip())
    except Exception as e:
        print(f"Error in listen_for_events: {e}")


def listen_for_events_for_not_dynamic():
    try:
        socket_path = os.path.join(
            os.environ.get("XDG_RUNTIME_DIR", "/run/user/1000"),
            f"hypr/{os.environ.get('HYPRLAND_INSTANCE_SIGNATURE', '')}/.socket2.sock",
        )
        if DEBUG:
            print(f"Connecting to socket at {socket_path}")

        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.connect(socket_path)
            with client.makefile("r") as stream:
                for line in stream:
                    handle_for_not_dynamic(line.strip())
    except Exception as e:
        print(f"Error in listen_for_events: {e}")


def check_nwg_dock_hyprland():
    return shutil.which("nwg-dock-hyprland") is not None


def windows_data():
    result = json.loads(
        subprocess.run(
            ["hyprctl", "clients", "-j"], capture_output=True, text=True
        ).stdout.strip(),
    )
    return result


def write_file(path: str, content: str) -> None:
    with open(path, "w") as f:
        f.write(content)


if __name__ == "__main__":
    pkill_dock = lambda: subprocess.run(["pkill", "-f", "nwg-dock-hyprland"])
    state_dock = pathlib.Path.home() / ".cache" / "state_dock"

    def read_state_dock() -> str:
        if not pathlib.Path(state_dock).exists():
            write_file(str(state_dock), "enable")
        with open(state_dock, "r") as f:
            return f.read()

    read_state = read_state_dock()

    def toggle_dock_main():
        tmp_file = "/tmp/dock_toggle"
        if pathlib.Path(tmp_file).exists():
            pathlib.Path(tmp_file).unlink()
            write_file(str(state_dock), "enable")
            main()
        else:
            write_file(tmp_file, "disable")
            write_file(str(state_dock), "disable")
            pkill_dock()

    if check_nwg_dock_hyprland():
        parser = argparse.ArgumentParser(description="hyprdock")
        parser.add_argument(
            "-t", "--toggle", action="store_true", help="Toggle hyprdock hide|show"
        )
        parser.add_argument(
            "-d", "--disable", action="store_true", help="Kill hyprdock"
        )
        parser.add_argument(
            "-a", "--autostart", action="store_true", help="Autostart hyprdock"
        )
        parser.add_argument(
            "-e", "--enable", action="store_true", help="Autostart hyprdock"
        )

        args = parser.parse_args()

        if args.autostart:
            if read_state == "disable":
                ...
            elif read_state == "enable":
                main()

        elif args.disable:
            pkill_dock()
            write_file(str(state_dock), "disable")

        elif args.enable:
            main()
            write_file(str(state_dock), "enable")

        if args.toggle:
            toggle_dock_main()

        else:
            if read_state == "enable":
                while True:
                    active_windows = str(windows_data())

                    if active_windows == "[]":
                        start_dock(
                            "-x",
                            UPDATE_DOCK=True,
                        )
                    else:
                        pkill_dock()
                        start_dock(
                            "-r",
                            UPDATE_DOCK=True,
                        )
                        pkill_dock()
                        toggle_dock("hide")
                        main()
                        break

    else:
        print("nwg-dock-hyprland not found")
        subprocess.run(["notify-send", "nwg-dock-hyprland not found"])
