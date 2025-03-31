#!/usr/bin/env python

# network_signal.py
# https://github.com/maarutan
# Copyright (c) 2025 |  by maaru \ maarutan

import os, subprocess, pathlib
from time import sleep

# DONE: ####   -----=== global variables ===-----   ####

DEBUG = False  # show print no write current
DELAY_TIME = 1  # while True delay time


PADDING = [0, 0]  # padding_left { icon } padding_right
WIFI_ICON = "round"  # round, square, number, triangle
NOT_CONNECTED_ICON = "󰌙"
CACHE_FILE_CONNECTED = os.getenv("HOME") + "/.cache/current_signal_network"  # type: ignore
CACHE_FILE_NO_CONNECTED = os.getenv("HOME") + "/.cache/current_signal_no_network"  # type: ignore
CACHE_FILE_CURRENT_ICON = os.getenv("HOME") + "/.cache/cache_file_current_icon"  # type: ignore

# INFO: ####   -----=== logic ===-----   ####


def main():
    try:
        if DEBUG:
            while True:
                print()
                sleep(DELAY_TIME)
                print()
                print(f"ethernet_no_internet: {is_ethernet_no_connected()}")
                print(f"wifi_no_internet: {is_wifi_connected_no_internet()}")
                print()
                print(f"signal: {get_signal()}")
                print(f"icon: {icons()}")
                print(f"icon_theme: {WIFI_ICON}")
                print()
                print(f"cache file connected: {read_cache_file_connected()}")
                print()
                print(f"get_check_connected: {get_check_connected()}")
                print(
                    f"read_current_not_connected_internet: {read_current_not_connected_internet()}"
                )
        else:
            print_icon()

    except KeyboardInterrupt:
        print("\n  cancel <3")


def print_icon():
    icon = str(padding_icons(icons()))
    if not icon:
        try:
            with open(CACHE_FILE_CURRENT_ICON, "r") as f:
                cached_icon = f.read().strip()
                if cached_icon:
                    print(cached_icon)
                    return
        except FileNotFoundError:
            pass

    with open(CACHE_FILE_CURRENT_ICON, "w") as f:
        f.write(icon)
    print(icon)


def padding_icons(icons):
    left_pad, right_pad = PADDING
    return " " * left_pad + icons + " " * right_pad


def shell(command) -> str:
    blacklist = {"poweroff", "reboot", "rm", "shutdown"}
    cmd = command.split()[0]

    if cmd in blacklist:
        return ""

    return subprocess.run(
        command, shell=True, text=True, capture_output=True
    ).stdout.strip()


def check_network_manager() -> str:
    if shell("command -v nmcli"):
        return ""
    else:
        return "nmcli not found"


def get_check_connected() -> str:
    wifi = shell("nmcli -t -f DEVICE,TYPE,STATE dev | grep 'wifi:connected'")
    ethernet = shell("nmcli -t -f DEVICE,TYPE,STATE dev | grep 'ethernet:connected'")
    if ethernet:
        with open(CACHE_FILE_CONNECTED, "w") as f:
            f.write("ethernet")
        return "ethernet"

    elif wifi:
        with open(CACHE_FILE_CONNECTED, "w") as f:
            f.write("wifi")
            return "wifi"

    elif wifi and ethernet:
        with open(CACHE_FILE_CONNECTED, "w") as f:
            f.write("ethernet")
        return "ethernet"

    return "no_connection"


def read_cache_file_connected() -> str:
    with open(CACHE_FILE_CONNECTED, "r") as f:
        return f.read().strip()


def get_check_connected_no_internet():
    wifi = is_wifi_connected_no_internet()
    ethernet = is_ethernet_no_connected()

    if ethernet:
        with open(CACHE_FILE_NO_CONNECTED, "w") as f:
            f.write("ethernet_no_internet")
        return "ethernet_no_internet"

    elif wifi:
        with open(CACHE_FILE_NO_CONNECTED, "w") as f:
            f.write("wifi_no_internet")
        return "wifi_no_internet"

    elif wifi and ethernet:
        with open(CACHE_FILE_NO_CONNECTED, "w") as f:
            f.write("ethernet_no_internet")

    return "no_connection"


def read_current_not_connected_internet():
    if not pathlib.Path(CACHE_FILE_NO_CONNECTED).exists():
        with open(CACHE_FILE_NO_CONNECTED, "w") as f:
            f.write("ethernet_no_internet")

    with open(CACHE_FILE_NO_CONNECTED, "r") as f:
        return f.read()


def get_signal() -> int | None:
    connection_type = get_check_connected()
    if connection_type != "wifi":
        return None

    result = shell(
        "nmcli -t -f IN-USE,SIGNAL dev wifi | grep '*' | awk -F: '{print $2}'"
    )
    if result == "" or not result or result == None:
        return None
    return int(result)


def is_ethernet_no_connected() -> bool:
    connection_type = get_check_connected()
    if connection_type != "ethernet":
        return False

    ip_check = shell("nmcli -t -f DEVICE,STATE,IP4 dev show | grep ethernet")

    if "connected" in ip_check and "IP4.ADDRESS" not in ip_check:
        return True

    return False


def is_wifi_connected_no_internet() -> bool:
    connection_type = get_check_connected()
    if connection_type != "wifi":
        return False

    ip_check = shell("nmcli -t -f DEVICE,STATE,IP4.ADDRESS dev show | grep wifi")

    if "connected" in ip_check and "IP4.ADDRESS" not in ip_check:
        return True

    internet_check = shell("ping -c 1 8.8.8.8")
    if "1 received" not in internet_check:
        return True

    return False


def icons():
    signal = get_signal()
    connection_type = get_check_connected()
    connection_type_no_internet = get_check_connected_no_internet()

    rounded_wifi = {
        65: "󰤨",
        55: "󰤥",
        40: "󰤢",
        20: "󰤟",
        10: "󰤯",
        "no connection": "󰤮",
    }
    rounded_wifi_no_internet = {
        65: "󰤩",
        55: "󰤦",
        40: "󰤣",
        20: "󰤠",
        10: "󰤠",
        "no connection": "󰤮",
    }

    square_wifi = {
        65: "▁▃▅▇",
        55: "▁▃▅⎽",
        40: "▁▃⎽⎽",
        20: "▁⎽⎽⎽",
        10: "⎽⎽⎽⎽",
        "no connection": NOT_CONNECTED_ICON,
    }

    number_wifi = f"wifi: {signal}%"
    number_wifi_no_internet = f"wifi: {str(signal)}%!"

    square_wifi_no_internet = {
        65: "▁▃▅▇!",
        55: "▁▃▅⎽!",
        40: "▁▃⎽⎽!",
        20: "▁⎽⎽⎽!",
        10: "⎽⎽⎽⎽!",
        "no connection": NOT_CONNECTED_ICON,
    }

    triangle_wifi = {
        65: "󰣺",
        55: "󰣸",
        40: "󰣶",
        20: "󰣴",
        10: "󰣾",
        "no connection": "󰣽",
    }
    triangle_wifi_no_internet = {
        65: "󰣻",
        55: "󰣹",
        40: "󰣷",
        20: "󰣵",
        10: "󰣵",
        "no connection": "󰣽",
    }

    ethernet = {
        "ethernet": "󰈀",
        "no connection": "󱘖",
    }

    ethernet_no_internet = {
        "ethernet": "󰈀 !",
        "no connection": "󱘖",
    }

    if connection_type == "wifi":
        if signal:
            if connection_type_no_internet != "wifi_no_internet":
                if WIFI_ICON == "round":
                    return next(
                        (
                            icon
                            for level, icon in sorted(
                                {
                                    k: v
                                    for k, v in rounded_wifi.items()
                                    if isinstance(k, int)
                                }.items(),
                                reverse=True,
                            )
                            if signal >= level
                        ),
                        rounded_wifi["no connection"],
                    )
                elif WIFI_ICON == "square":
                    return next(
                        (
                            icon
                            for level, icon in sorted(
                                {
                                    k: v
                                    for k, v in square_wifi.items()
                                    if isinstance(k, int)
                                }.items(),
                                reverse=True,
                            )
                            if signal >= level
                        ),
                        square_wifi["no connection"],
                    )
                elif WIFI_ICON == "triangle":
                    return next(
                        (
                            icon
                            for level, icon in sorted(
                                {
                                    k: v
                                    for k, v in triangle_wifi.items()
                                    if isinstance(k, int)
                                }.items(),
                                reverse=True,
                            )
                            if signal >= level
                        ),
                        triangle_wifi["no connection"],
                    )
                elif WIFI_ICON == "number":
                    return number_wifi

            elif connection_type_no_internet == "wifi_no_internet":
                if WIFI_ICON == "round":
                    return next(
                        (
                            icon
                            for level, icon in sorted(
                                {
                                    k: v
                                    for k, v in rounded_wifi_no_internet.items()
                                    if isinstance(k, int)
                                }.items(),
                                reverse=True,
                            )
                            if signal >= level
                        ),
                        rounded_wifi_no_internet["no connection"],
                    )
                elif WIFI_ICON == "square":
                    return next(
                        (
                            icon
                            for level, icon in sorted(
                                {
                                    k: v
                                    for k, v in square_wifi_no_internet.items()
                                    if isinstance(k, int)
                                }.items(),
                                reverse=True,
                            )
                            if signal >= level
                        ),
                        rounded_wifi_no_internet["no connection"],
                    )
                elif WIFI_ICON == "triangle":
                    return next(
                        (
                            icon
                            for level, icon in sorted(
                                {
                                    k: v
                                    for k, v in triangle_wifi_no_internet.items()
                                    if isinstance(k, int)
                                }.items(),
                                reverse=True,
                            )
                            if signal >= level
                        ),
                        rounded_wifi_no_internet["no connection"],
                    )
                elif WIFI_ICON == "number":
                    return number_wifi_no_internet

    elif connection_type == "ethernet":
        return ethernet["ethernet"]

    elif read_current_not_connected_internet() == "ethernet_no_internet":
        return ethernet_no_internet["ethernet"]

    else:
        cahce = read_cache_file_connected()
        if cahce == "ethernet":
            return ethernet["no connection"]

        if WIFI_ICON == "round" and cahce == "wifi":
            return rounded_wifi["no connection"]
        elif WIFI_ICON == "triangle" and cahce == "wifi":
            return triangle_wifi["no connection"]
        elif WIFI_ICON == "square" and cahce == "wifi":
            return square_wifi["no connection"]
        elif WIFI_ICON == "number" and cahce == "wifi":
            return NOT_CONNECTED_ICON

        return NOT_CONNECTED_ICON


if __name__ == "__main__":
    main()
