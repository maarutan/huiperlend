#!/usr/bin/env python3

import subprocess, pathlib


def reload():
    subprocess.run([pathlib.Path(__file__).parent / "toggle_polybar.py"], shell=True)
    subprocess.run([pathlib.Path(__file__).parent / "runner.py"], shell=True)


if __name__ == "__main__":
    reload()
