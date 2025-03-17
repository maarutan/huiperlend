#!/usr/bin/env python3

# brightness_control in python
# https://github.com/maarutan
# Copyright (c) 2025 |  by maaru \ maarutan


import subprocess
import pathlib
import sys
import shutil

# DONE: ----=== Global Variables ===----

brightness_icon = "dynamic"  # dynamic, static, moon_sun, none
DELAY_TIME = 2000  # milliseconds
PROGRESS_LINE = True
CACHE_FILE_SYSTEM_THEME = pathlib.Path.home() / ".cache" / "system_theme"


BRIGHTNESS_CONTENT = lambda brightness: f"  *･ﾟ✧ {brightness}% ✧･ﾟ*"

# INFO: ----=== Logic ===----


def get_brightness() -> int:
    current_brightness = int(
        subprocess.run(
            ["brightnessctl", "get"], stdout=subprocess.PIPE, text=True
        ).stdout.strip()
    )
    max_brightness = int(
        subprocess.run(
            ["brightnessctl", "max"], stdout=subprocess.PIPE, text=True
        ).stdout.strip()
    )
    return round(100 * (current_brightness / max_brightness))


def set_brightness(brightness_percent: int):
    max_brightness = int(
        subprocess.run(
            ["brightnessctl", "max"], stdout=subprocess.PIPE, text=True
        ).stdout.strip()
    )
    brightness_value = int(max_brightness * (brightness_percent / 100))
    subprocess.run(["brightnessctl", "set", str(brightness_value)])


def get_cache_file_system_theme():
    theme_file = CACHE_FILE_SYSTEM_THEME
    if not theme_file.exists():
        theme_file.parent.mkdir(parents=True, exist_ok=True)
        with open(theme_file, "w") as f:
            f.write("dark")
        return "dark"

    try:
        with open(theme_file, "r") as f:
            return f.read().strip()
    except:
        return "dark"


def get_icons():
    get_level = get_brightness()
    system_theme = get_cache_file_system_theme()
    path = pathlib.Path(__file__).parent / ".icons"

    if system_theme == "dark":
        path = path / "dark"
    elif system_theme == "light":
        path = path / "light"

    icons = {
        10: f"brightness-{system_theme}_10.svg",
        20: f"brightness-{system_theme}_20.svg",
        30: f"brightness-{system_theme}_30.svg",
        40: f"brightness-{system_theme}_40.svg",
        50: f"brightness-{system_theme}_50.svg",
        60: f"brightness-{system_theme}_60.svg",
        70: f"brightness-{system_theme}_70.svg",
        80: f"brightness-{system_theme}_80.svg",
        90: f"brightness-{system_theme}_90.svg",
        100: f"brightness-{system_theme}_100.svg",
    }
    if brightness_icon == "dynamic":
        for key in sorted(icons.keys(), reverse=True):
            if get_level >= key:
                return path / icons[key]

        return path / icons[10]
    elif brightness_icon == "static":
        return path / icons[100]
    elif brightness_icon == "moon_sun":
        if get_level < 50:
            return path / icons[20]
        else:
            return path / icons[100]
    elif brightness_icon == "none":
        return

    return path / icons[100]


def send_notification(brightness: int):
    icon_path = get_icons()
    if PROGRESS_LINE:
        subprocess.run(
            [
                "notify-send",
                "-i",
                str(icon_path),
                "-t",
                str(DELAY_TIME),
                "-h",
                f"int:value:{brightness}",
                "-r",
                "9999",
                BRIGHTNESS_CONTENT(brightness),
            ]
        )
    else:
        subprocess.run(
            [
                "notify-send",
                "-i",
                str(icon_path),
                "-t",
                str(DELAY_TIME),
                "-r",
                "9999",
                BRIGHTNESS_CONTENT(brightness),
            ]
        )


def check_brightness():
    return shutil.which("brightnessctl")


def check_notify_send():
    return shutil.which("notify-send")


def main():
    if not check_brightness():
        subprocess.run(["notify-send", "-t", "2000", "brightnessctl", "не найден"])
        sys.exit(1)

    if not check_notify_send():
        subprocess.run(["notify-send", "-t", "2000", "notify-send", "не найден"])
        sys.exit(1)

    if len(sys.argv) != 2 or sys.argv[1] not in {"up", "down"}:
        sys.exit(1)

    current_brightness = get_brightness()

    if sys.argv[1] == "up" and current_brightness < 100:
        new_brightness = min(current_brightness + 5, 100)
        set_brightness(new_brightness)
        send_notification(new_brightness)

    elif sys.argv[1] == "down" and current_brightness > 0:
        new_brightness = max(current_brightness - 5, 0)
        set_brightness(new_brightness)
        send_notification(new_brightness)


if __name__ == "__main__":
    main()
