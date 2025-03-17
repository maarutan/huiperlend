#!/usr/bin/env python3

import subprocess, time


def killall_polybar():
    subprocess.run(["killall", "-q", "polybar"])


def launch_bar1_and_bar2():
    subprocess.run(
        ["echo", "'---'", "|", "tee", "-a", "/tmp/polybar1.log", "/tmp/polybar2.log"]
    )


def start_polybar():
    subprocess.run(["polybar"])


if __name__ == "__main__":
    try:
        killall_polybar()
        launch_bar1_and_bar2()
        start_polybar()
    except KeyboardInterrupt:
        print("\n  canceled")
