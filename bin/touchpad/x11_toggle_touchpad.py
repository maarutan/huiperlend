#!/usr/bin/env python3

# toggle_touchpad.py
# github: https://github.com/maarutan
# (c) by maaru.tan

import subprocess
import sys
import pathlib

# Global variables
TMP_FILE = "/tmp/touchpad_tmp_config"
icons = pathlib.Path(__file__).parent / ".icons" / "touchpad.svg"


def shell(command: list[str]) -> str | None:
    blacklist = {"poweroff", "reboot", "rm", "shutdown"}

    if command[0] in blacklist:
        print(f"Skipping dangerous command: {' '.join(command)}")
        return None

    try:
        return subprocess.check_output(command, text=True).strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None


def notify_send(
    message: str = "",
    WARN: bool = False,
    INFO: bool = False,
    icon: str = "",
    notify_id: int = 0,
):
    icon = (
        (
            "dialog-warning"
            if WARN
            else "dialog-information"
            if INFO
            else "dialog-message"
        )
        if icon == ""
        else icon
    )
    subprocess.run(["notify-send", "-r", str(notify_id), "--icon", icon, message])


def find_touchpad_id() -> str | None:
    result = shell(["xinput", "list"])
    if not result:
        return None

    touchpad_line = next(
        (line for line in result.splitlines() if "Touchpad" in line), None
    )
    if not touchpad_line:
        return None

    parts = touchpad_line.split()
    touchpad_id = next((p.split("=")[1] for p in parts if p.startswith("id=")), None)

    if touchpad_id:
        pathlib.Path(TMP_FILE).write_text(touchpad_id)

    return touchpad_id


def read_tmp_file() -> str | None:
    path = pathlib.Path(TMP_FILE)
    if path.exists():
        return path.read_text().strip()
    return None


def get_touchpad_id() -> str | None:
    touchpad_id = read_tmp_file() or find_touchpad_id()

    if not touchpad_id:
        notify_send("Touchpad not found", WARN=True)
        sys.exit(1)

    return touchpad_id


def get_touchpad_status(touchpad_id: str) -> bool:
    result = shell(["xinput", "list-props", touchpad_id])
    if not result:
        return False

    enabled_line = next(
        (line for line in result.splitlines() if "Device Enabled" in line), None
    )

    if not enabled_line:
        notify_send("Touchpad settings not found", WARN=True)
        return False

    status = enabled_line.split()[-1]
    return status == "1"


def toggle_touchpad():
    touchpad_id = get_touchpad_id()
    is_enabled = get_touchpad_status(touchpad_id)  # type: ignore

    if is_enabled:
        shell(["xinput", "disable", touchpad_id])  # type: ignore
        notify_send(f"Touchpad turned off", icon=str(icons), notify_id=9999)
    else:
        shell(["xinput", "enable", touchpad_id])  # type: ignore
        notify_send(f"Touchpad turned on", icon=str(icons), notify_id=9999)


if __name__ == "__main__":
    toggle_touchpad()
