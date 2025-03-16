#!/usr/bin/env python3

import subprocess
import pathlib
import sys
import time
import json


settings_file = pathlib.Path(__file__).parent.parent / "settings.json"


def load_settings():
    if settings_file.exists():
        with open(settings_file, "r") as f:
            return json.load(f)
    return {"smart_gaps": {"ENABLED": True, "SMART_GAPS_HOR": 15, "SMART_GAPS_VET": 0}}


def save_settings(settings):
    with open(settings_file, "w") as f:
        json.dump(settings, f, indent=4)


settings = load_settings()


smart_gaps_enabled = settings["smart_gaps"].get("ENABLED", True)


smart_gaps_hor = settings["smart_gaps"].get("SMART_GAPS_HOR", 15)
smart_gaps_vet = settings["smart_gaps"].get("SMART_GAPS_VET", 0)

cache_file = pathlib.Path(__file__).parent.parent.parent / ".cache" / "current_gaps"
DEBUG = False


def default_settings_gaps():
    return 15


def default_settings_paddings():
    return 0, 0, 0, 0


def write_cache_current_gaps():
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    if not cache_file.exists():
        cache_file.write_text(str(default_settings_gaps()))


def get_window_count():
    result = subprocess.run(
        ["bspc", "query", "-N", "-d", "focused"], stdout=subprocess.PIPE, text=True
    )
    windows = result.stdout.strip().split("\n")
    return len(windows) if windows[0] else 0


def read_cache_current_gaps():
    if cache_file.exists():
        return int(cache_file.read_text())
    return default_settings_gaps()


def smart_gaps(**kwargs):
    settings["smart_gaps"].update(kwargs)
    save_settings(settings)


def main():
    try:
        if not smart_gaps_enabled:
            return

        if get_window_count() == 1:
            write_cache_current_gaps()
            subprocess.run(
                [
                    "bspc",
                    "config",
                    "window_gap",
                    str(settings["smart_gaps"]["SMART_GAPS_HOR"]),
                ]
            )
            subprocess.run(
                [
                    "bspc",
                    "config",
                    "left_padding",
                    str(settings["smart_gaps"]["SMART_GAPS_VET"]),
                ]
            )
            subprocess.run(
                [
                    "bspc",
                    "config",
                    "right_padding",
                    str(settings["smart_gaps"]["SMART_GAPS_VET"]),
                ]
            )
        else:
            cached_gaps = read_cache_current_gaps()
            subprocess.run(["bspc", "config", "window_gap", str(cached_gaps)])

            left, right, top, bottom = default_settings_paddings()
            subprocess.run(["bspc", "config", "left_padding", str(left)])
            subprocess.run(["bspc", "config", "right_padding", str(right)])
            subprocess.run(["bspc", "config", "top_padding", str(top)])
            subprocess.run(["bspc", "config", "bottom_padding", str(bottom)])
    except Exception as e:
        print(f"Ошибка: {e}")


def main_loop():
    while True:
        try:
            if DEBUG:
                print(f"Window count: {get_window_count()}")
                print(f"Cache current gaps: {read_cache_current_gaps()}\n")
                time.sleep(0.1)
            else:
                main()
                time.sleep(0.1)
        except KeyboardInterrupt:
            sys.exit(0)
