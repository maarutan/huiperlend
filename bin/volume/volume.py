#!/usr/bin/env python3

import subprocess
import pathlib
import sys
import shutil

# ----=== Global Variables ===----

SEND_ID = 9999
VOLUME_THEME = "twist"  # loudmouth, twist
DELAY_TIME = 2000  # milliseconds
PROGRESS_LINE = True
CACHE_FILE_SYSTEM_THEME = pathlib.Path.home() / ".cache" / "system_theme"
VOLUME_CONTENT_MUTE = "   (づ｡◕‿‿◕｡)づ"
VOLUME_CONTENT = lambda volume: f"  *･ﾟ✧ {volume}% ✧･ﾟ*"


# ----=== Logic ===----


def shell(command):
    result = subprocess.run(
        command,
        shell=True,
        text=True,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip() if result.stdout else None


def get_volume() -> int:
    result = shell(
        "pactl get-sink-volume @DEFAULT_SINK@ | grep -oP '\\d+%' | head -n 1 | tr -d '%'"
    )
    return int(result) if result and result.isdigit() else 0


def is_mute() -> bool:
    output = shell("pactl get-sink-mute @DEFAULT_SINK@")
    return "yes" in output.lower() if output else False


def is_mic_mute() -> bool:
    output = shell("pactl get-source-mute @DEFAULT_SOURCE@")
    return "yes" in output.lower() if output else False


def get_system_theme():
    if CACHE_FILE_SYSTEM_THEME.exists():
        return CACHE_FILE_SYSTEM_THEME.read_text().strip()

    CACHE_FILE_SYSTEM_THEME.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE_SYSTEM_THEME.write_text("dark")
    return "dark"


class Icons:
    def __init__(self):
        self.volume_level = get_volume()
        self.system_theme = get_system_theme()

        if VOLUME_THEME == "loudmouth":
            self.path = (
                pathlib.Path(__file__).parent
                / ".icons"
                / "loudmouth"
                / self.system_theme
            )
            self.icons = {
                10: f"volume_{self.system_theme}_10.svg",
                30: f"volume_{self.system_theme}_30.svg",
                60: f"volume_{self.system_theme}_60.svg",
                90: f"volume_{self.system_theme}_90.svg",
                9999: f"volume_{self.system_theme}_mute.svg",
                99999: f"volume_{self.system_theme}_microphone_off.svg",
                999999: f"volume_{self.system_theme}_microphone_on.svg",
            }
        elif VOLUME_THEME == "twist":
            self.path = (
                pathlib.Path(__file__).parent / ".icons" / "twist" / self.system_theme
            )
            self.icons = {
                0: "vol-0.svg",
                10: "vol-10.svg",
                15: "vol-15.svg",
                20: "vol-20.svg",
                25: "vol-25.svg",
                30: "vol-30.svg",
                35: "vol-35.svg",
                40: "vol-40.svg",
                45: "vol-45.svg",
                50: "vol-50.svg",
                55: "vol-55.svg",
                60: "vol-60.svg",
                65: "vol-65.svg",
                70: "vol-70.svg",
                75: "vol-75.svg",
                80: "vol-80.svg",
                85: "vol-85.svg",
                90: "vol-90.svg",
                95: "vol-95.svg",
                100: "vol-100.svg",
                9999: "vol-mute.svg",
                99999: "vol-micro-mute.svg",
                999999: "vol-micro.svg",
            }

    def get_mute_icon(self):
        return self.path / self.icons[9999] if is_mute() else None

    def get_microphone_icon(self):
        return (
            self.path / self.icons[99999]
            if is_mic_mute()
            else self.path / self.icons[999999]
        )

    def get_volume_icon(self):
        for key in sorted(self.icons.keys(), reverse=True):
            if self.volume_level >= key:
                return self.path / self.icons[key]
        return self.path / self.icons[10]


def adjust_volume(delta: int):
    current_volume = get_volume()
    new_volume = max(0, min(100, current_volume + delta))

    shell("pactl set-sink-mute @DEFAULT_SINK@ 0")
    shell(f"pactl set-sink-volume @DEFAULT_SINK@ {new_volume}%")
    return new_volume


def notify_send_mute():
    icon_path = Icons().get_mute_icon()
    shell(
        f'notify-send -i "{icon_path}" -t {DELAY_TIME} -r {SEND_ID} "{VOLUME_CONTENT_MUTE}"'
    )


def send_notification(volume: int, progress: bool = True):
    icon_path = Icons().get_volume_icon()
    if progress and PROGRESS_LINE:
        shell(
            f'notify-send -i "{icon_path}" -t {DELAY_TIME} -h int:value:{volume} -r {SEND_ID} "{VOLUME_CONTENT(volume)}"'
        )
    else:
        shell(
            f'notify-send -i "{icon_path}" -t {DELAY_TIME} -r {SEND_ID} "{VOLUME_CONTENT(volume)}"'
        )


def toggle_microphone():
    shell("pactl set-source-mute @DEFAULT_SOURCE@ toggle")
    icon_path = Icons().get_microphone_icon()
    message = VOLUME_CONTENT_MUTE if is_mic_mute() else "🎤 Microphone Unmuted"
    shell(f'notify-send -i "{icon_path}" -t {DELAY_TIME} -r {SEND_ID} "{message}"')


def check_pactl():
    return shutil.which("pactl")


def check_notify_send():
    return shutil.which("notify-send")


def send_notification_for_mute():
    volume = get_volume()
    icon_path = Icons().get_volume_icon()

    if is_mute():
        icon_path = Icons().get_mute_icon()
        shell(
            f'notify-send -i "{icon_path}" -t {DELAY_TIME} -r {SEND_ID} "{VOLUME_CONTENT_MUTE}"'
        )
    else:
        shell(
            f'notify-send -i "{icon_path}" -t {DELAY_TIME} -h int:value:{volume} -r {SEND_ID} "{VOLUME_CONTENT(volume)}"'
        )


def main():
    if not check_pactl():
        shell("notify-send -t 2000 'pactl not found'")
        return

    if not check_notify_send():
        shell("notify-send -t 2000 'notify-send not found'")
        return

    if len(sys.argv) != 2 or sys.argv[1] not in {"up", "down", "mute", "mic"}:
        return

    if sys.argv[1] == "up":
        send_notification(adjust_volume(5), progress=True)
    elif sys.argv[1] == "down":
        send_notification(adjust_volume(-5), progress=True)

    elif sys.argv[1] == "mute":
        shell("pactl set-sink-mute @DEFAULT_SINK@ toggle")
        send_notification_for_mute()

    elif sys.argv[1] == "mic":
        toggle_microphone()


if __name__ == "__main__":
    main()
