#!/usr/bin/env python3

import os, pathlib
from subprocess import run as shell

ROFI_CONFIG = pathlib.Path(__file__).parent.parent / "assets/rofi_theme/types.rasi"
GALLERY = (
    pathlib.Path(__file__).parent.parent / "assets" / "rofi_theme" / "gallery.rasi"
)
ROW = pathlib.Path(__file__).parent.parent / "assets" / "rofi_theme" / "row.rasi"
ASSETS = pathlib.Path(__file__).parent.parent / "assets/types"
RESULT = pathlib.Path(__file__).parent.parent / "assets" / "rofi_theme" / "wall.rasi"


def get_img():
    array = []
    extensions = (".jpg", ".png")
    for file in os.listdir(ASSETS):
        parent_file = os.path.join(ASSETS, file)
        if os.path.isfile(parent_file) and file.endswith(extensions):
            array.append(f"{file}\x00icon\x1f{ASSETS}/{file}")
    return array


def rofi():
    result = shell(
        ["rofi", "-theme", ROFI_CONFIG, "-dmenu"],
        input="\n".join(get_img()),
        text=True,
        capture_output=True,
    )
    return result.stdout.strip() if result.stdout else None


def pick_type():
    selection = rofi()
    if not selection:
        exit(0)

    file_map = {
        "gallery.png": GALLERY,
        "row.png": ROW,
    }

    if selection.lower() in file_map:
        file_path = file_map[selection.lower()]
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                content = f.read()
            with open(RESULT, "w") as f:
                f.write(content)
        else:
            print(f"config {file_path} no found !")


if __name__ == "__main__":
    pick_type()
