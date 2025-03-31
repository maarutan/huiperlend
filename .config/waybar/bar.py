#!/usr/bin/env python
import re
import pathlib
import json
import argparse
import subprocess

CONFIG_JSON = pathlib.Path(__file__).parent / "config.jsonc"
DIR_NAME_COLORSHEME = "theme"
TMP_FILE = "/tmp/bar_toggle"

ENABLE_BAR = (
    lambda WRITE=False: (
        pathlib.Path(TMP_FILE).unlink() if pathlib.Path(TMP_FILE).exists() else None,
        subprocess.run(["waybar", "-c", str(CONFIG_JSON), "-s", str(read_jsonc())]),
    )
    if WRITE
    else None
)

DISABLE_BAR = (
    lambda WRITE=False: (
        write_file(TMP_FILE, "disable"),
        subprocess.run(["pkill", "-f", "waybar"]),
    )
    if WRITE
    else None
)

AUTOSTART = (
    lambda: DISABLE_BAR() if pathlib.Path(TMP_FILE).exists() else ENABLE_BAR(WRITE=True)
)

TOGGLE = (
    lambda: ENABLE_BAR(WRITE=True)
    if pathlib.Path(TMP_FILE).exists()
    else DISABLE_BAR(WRITE=True)
)


def main(args):
    if args.theme:
        theme_path = CONFIG_JSON.parent / DIR_NAME_COLORSHEME / args.theme / "style.css"
        target_path = CONFIG_JSON.parent / "current.css"
        with open(theme_path, "r") as o:
            write_file(str(target_path), o.read())

    if args.enable:
        ENABLE_BAR(True)
    if args.disable:
        DISABLE_BAR(True)
    if args.autostart:
        AUTOSTART()
    if args.toggle:
        TOGGLE()
    if args.theme is None:
        ENABLE_BAR(True)


def write_file(path: str, content: str):
    with open(path, "w") as f:
        f.write(content)


def read_jsonc():
    with open(CONFIG_JSON, "r") as f:
        jsonc_content = f.read()
        jsonc_content = re.sub(r"//.*", "", jsonc_content)
        jsonc_content = re.sub(r",\s*(]|\})", r"\1", jsonc_content)
        data = json.loads(jsonc_content)
        return (
            pathlib.Path(__file__).parent / DIR_NAME_COLORSHEME / data["style-config"]
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Starter Bar")
    parser.add_argument("theme", nargs="?", help="Theme name")
    parser.add_argument("-d", "--disable", action="store_true", help="Disable Bar")
    parser.add_argument("-e", "--enable", action="store_true", help="Enable Bar")
    parser.add_argument("-t", "--toggle", action="store_true", help="Toggle Bar")
    parser.add_argument("-a", "--autostart", action="store_true", help="Autostart Bar")

    args, unknown = parser.parse_known_args()

    try:
        main(args)
    except KeyboardInterrupt:
        print("~ cancel ^^")
