#!/usr/bin/env python3

from images.launcher import wall_start as images
from live.launcher import wall_start as live
from logic.choice_theme import CACHE_TYPE
from subprocess import run as shell, os


def read_cache_type() -> str:
    with open(CACHE_TYPE, "r") as f:
        file = f.read().strip()
        return file


print(read_cache_type())

try:
    if read_cache_type() == "live":
        shell(["pkill", "-f", "swww-demon"])
        live()
    elif read_cache_type() == "static":
        images()
    elif read_cache_type() == "":
        images()

except KeyboardInterrupt:
    print("\n  cancel")
