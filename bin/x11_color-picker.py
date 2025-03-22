#!/usr/bin/env python3

# xcolor-picker.py with gpick
# github: https://github.com/maarutan
# (c) by maaru.tan


import subprocess, shutil, argparse, os
from pathlib import Path

# DONE: -----=== Global Vars ===-----

VI_MODE = True
NOCAPS = True
EXPIRE_TIME = 5000


TEMP_DIR = Path("/tmp/xcolor")
TEMP_DIR.mkdir(parents=True, exist_ok=True)
TML_FILE = "/tmp/vi-mode"


# INFO: -----=== logic ===-----


def pick_color():
    try:
        hex_color = subprocess.check_output(
            ["gpick", "-pso", "--no-newline"], text=True
        ).strip()
        if not hex_color:
            return None
        return hex_color
    except subprocess.CalledProcessError:
        return None


def create_color_image(hex_color):
    hex_code = hex_color.lstrip("#")
    file_path = TEMP_DIR / f"{hex_code}.png"

    subprocess.run(
        ["convert", "-size", "300x300", f"xc:{hex_color}", str(file_path)], check=True
    )
    return file_path


class vi_mode:
    def enable_vi_mode(self):
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

    def disable_vi_mode(self):
        if NOCAPS:
            subprocess.run(["setxkbmap", "-option", "ctrl:nocaps"])
        else:
            subprocess.run(["setxkbmap", "-option", ""])

        if os.path.exists(TML_FILE):
            os.remove(TML_FILE)

        subprocess.run(["notify-send", "Vi Mode OFF"])

    def toggle_vi_mode(self):
        if os.path.exists(TML_FILE):
            disable_vi_mode()
        else:
            enable_vi_mode()


def enable_vi_mode():
    keymap = [
        ("43", "left"),
        ("44", "down"),
        ("45", "up"),
        ("46", "right"),
    ]

    for keycode, direction in keymap:
        subprocess.run(
            [
                "xmodmap",
                "-e",
                f"keycode {keycode} = {direction} nosymbol {direction} nosymbol",
            ]
        )

    open(TML_FILE, "w").close()


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


def copy_to_clipboard(text):
    subprocess.run(["xclip", "-sel", "c"], input=text, text=True, check=True)


def check_gpick():
    return shutil.which("gpick") is not None


def send_notification(hex_color, icon_path):
    subprocess.run(
        [
            "notify-send",
            "-a",
            "XColor",
            "--icon",
            str(icon_path),
            "xcolor-pick",
            hex_color,
            "--expire-time",
            str(EXPIRE_TIME),
        ]
    )


def main():
    if not check_gpick():
        print("gpick is not installed")
        subprocess.run(["notify-send", "gpick is not installed"])
        return

    vi = vi_mode()
    vi.enable_vi_mode()

    hex_color = pick_color()
    if not hex_color:
        vi.disable_vi_mode()
        return

    icon_path = create_color_image(hex_color)
    copy_to_clipboard(hex_color)
    send_notification(hex_color, icon_path)

    vi.disable_vi_mode()


if __name__ == "__main__":
    main()
