#!/usr/bin/env python3

from images.launcher import read_current_wall, wall_start
from live.launcher import video_start
from logic.choice_theme import CACHE_TYPE
from subprocess import run as shell


def read_cache_type() -> str:
    with open(CACHE_TYPE, "r") as f:
        file = f.read().strip()
        return file


def live() -> None:
    selected_wall = read_current_wall()

    if not selected_wall:
        return

    if selected_wall.endswith((".mp4", ".mkv", ".webm", ".avi", ".mov")):
        video_start(selected_wall)

    elif selected_wall.endswith(("gif", "webp")):
        shell(["swww-daemon"])
        video_start(selected_wall)


try:
    if read_cache_type() == "live":
        live()
    else:
        wall_start()
except KeyboardInterrupt:
    print("\n  cancel")
