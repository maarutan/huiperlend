#!/usr/bin/env python3

LOAD_RANDOM_WALL = 0
LOAD_DEFAULT_WALL = 0
NOTIFY = 1
SCREEN_LOCK = 1

import os
import glob
from subprocess import run as shell
from PIL import Image
import random
import pathlib
from shutil import rmtree
import psutil

ROFI_THEME = pathlib.Path(__file__).parent.parent / "assets/rofi_theme/wall.rasi"
CACHE_THEME = pathlib.Path.home() / ".cache/current_theme"
CACHE_WALL = pathlib.Path.home() / ".cache/wallpapers_cache"
WALL_DIR = pathlib.Path.home() / "Pictures/wallpapers"
CURRENT_WALL = pathlib.Path.home() / ".cache/current_wallpaper"
STATIC_THEME_DIR = pathlib.Path.home() / "Pictures/wallpapers/static"

DEFAULT_WALLS = glob.glob(f"{WALL_DIR}/.default/default.*")
DEFAULT_WALL = DEFAULT_WALLS[0] if DEFAULT_WALLS else ""
TEMPLATE_STORAGE = "/tmp/wallpaper_storage"
TEMPLATE_STORAGE_THEME = "/tmp/wallpaper_storage_theme"

os.makedirs(CACHE_WALL, exist_ok=True)


def read_cache_theme() -> str:
    with open(CACHE_THEME, "r") as f:
        file = f.read().strip()
        return file


def get_theme_dir() -> tuple[list[str], list[str]]:
    """get_theme_dir[0] = name_theme, get_theme_dir[1] = path_name_theme"""
    names_theme = os.listdir(STATIC_THEME_DIR)
    path_name_theme = [os.path.join(STATIC_THEME_DIR, name) for name in names_theme]
    return names_theme, path_name_theme


def path_wall():
    with open(CACHE_THEME, "r") as f:
        file = f.read().strip()
        if not file:
            print("Theme file is empty.")
            return []
        for theme_dir in get_theme_dir()[1]:
            if file in theme_dir:
                try:
                    names = os.listdir(theme_dir)
                    paths = [os.path.join(theme_dir, name) for name in names]
                    return paths
                except FileNotFoundError:
                    print(f"Directory {theme_dir} not found.")
                    return []
    print("theme found.")
    return []


def path_dir_for_wall() -> str | None:
    with open(CACHE_THEME, "r") as f:
        file = f.read().strip()
        if not file:
            return ""
        for theme_dir in get_theme_dir()[1]:
            if file in theme_dir:
                try:
                    paths = os.path.join(theme_dir)
                    return paths
                except FileNotFoundError:
                    print(f"Directory {theme_dir} not found.")
                    return ""


def template_storage_theme(write):
    if write:
        with open(TEMPLATE_STORAGE_THEME, "w") as f:
            f.write(write)
    else:
        with open(TEMPLATE_STORAGE_THEME, "w") as f:
            f.write("")


def read_template_theme():
    if os.path.exists(TEMPLATE_STORAGE_THEME):
        with open(TEMPLATE_STORAGE_THEME, "r") as f:
            return f.read().strip()
    else:
        return ""


def check_changes_theme():
    template_storage_theme(read_cache_theme())
    current_theme = read_cache_theme()
    previous_theme = read_template_theme()

    if current_theme != previous_theme:
        try:
            rmtree(CACHE_WALL)
            print("Theme changed, cache cleared.")
            template_storage_theme(current_theme)
        except Exception as e:
            print(f"Error removing {CACHE_WALL}: {e}")
    else:
        print("Theme is the same, no need to clear cache.")


def template_storage(write):
    if write:
        with open(TEMPLATE_STORAGE, "w") as f:
            f.write(write)


def read_template():
    if os.path.exists(TEMPLATE_STORAGE):
        with open(TEMPLATE_STORAGE, "r") as f:
            return f.read().strip()
    return ""


def read_current_wall():
    if os.path.exists(CURRENT_WALL):
        with open(CURRENT_WALL, "r") as f:
            content = f.read().strip()
            template_storage(content)
            return content
    return ""


def storage_lockscreen():
    script_path = os.path.join(
        os.path.dirname(__file__), "..", "lockscreen", "betterlockscreen.py"
    )
    shell([script_path, "-g"])
    if NOTIFY:
        current_wall = read_current_wall()
        if current_wall and os.path.exists(current_wall):
            shell(
                [
                    "notify-send",
                    "-i",
                    current_wall,
                    "Lockscreen Updated",
                    f"Wallpaper: {os.path.basename(current_wall)}",
                ]
            )


def get_random_wall() -> str:
    walls = glob.glob(f"{path_dir_for_wall()}/*")
    return random.choice(walls) if walls else ""


def get_info_wall_thumbnail() -> list:
    check_changes_theme()
    current_wall = []
    extensions = (".jpg", ".png", ".jpeg", ".webp")
    paths = path_wall()

    for path in paths:  # pyright: ignore
        source_path = path
        cache_path = os.path.join(CACHE_WALL, os.path.basename(path))

        if os.path.isfile(source_path) and source_path.endswith(extensions):
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)

            if not os.path.exists(cache_path):
                with Image.open(source_path) as img:
                    img = img.convert("RGB")
                    width, height = img.size
                    aspect = 500 / min(width, height)
                    new_size = (int(width * aspect), int(height * aspect))
                    img = img.resize(new_size, Image.LANCZOS)  # pyright: ignore

                    left = (img.width - 500) / 2
                    top = (img.height - 500) / 2
                    right = left + 500
                    bottom = top + 500
                    img = img.crop((left, top, right, bottom))
                    img.save(cache_path, "JPEG", quality=90)

            current_wall.append(f"{os.path.basename(path)}\x00icon\x1f{cache_path}")

    return current_wall


def rofi() -> str:
    result = shell(
        ["rofi", "-theme", ROFI_THEME, "-dmenu"],
        input="\n".join(get_info_wall_thumbnail()),
        text=True,
        capture_output=True,
    )

    selected_wall = result.stdout.strip()

    if not selected_wall and LOAD_DEFAULT_WALL:
        if not DEFAULT_WALL:
            print("Error: No default wallpaper found.")
            return ""
        print("you didn't choose a wallpaper. Loading default wallpaper.")
        with open(CURRENT_WALL, "w") as f:
            f.write(DEFAULT_WALL)
        return DEFAULT_WALL

    if not selected_wall and LOAD_RANDOM_WALL:
        random_wall = get_random_wall()
        if not random_wall:
            print("Error: No random wallpaper found.")
            return ""
        print("you didn't choose a wallpaper. Loading random wallpaper.")
        with open(CURRENT_WALL, "w") as f:
            f.write(random_wall)
        return random_wall

    if not selected_wall:
        return exit(1)

    selected_path = (
        selected_wall
        if os.path.isabs(selected_wall)
        else os.path.join(path_dir_for_wall(), selected_wall)  # pyright: ignore
    )

    with open(CURRENT_WALL, "w") as f:
        f.write(selected_path)

    return selected_path


def is_process_running(process_name):
    for proc in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
        try:
            if proc.info["name"] and process_name.lower() in proc.info["name"].lower():
                return True
            if proc.info["cmdline"] and any(
                process_name in arg for arg in proc.info["cmdline"]
            ):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


def wall_start() -> None:
    if is_process_running("mpvpaper"):
        shell(["pkill", "-f", "mpvpaper"])

    if is_process_running("swww-daemon"):
        shell(
            [
                "swww",
                "img",
                rofi(),
                "--transition-type",
                "fade",
            ]
        )

    else:
        shell(["swww-daemon"])
        shell(
            [
                "swww",
                "img",
                rofi(),
                "--transition-type",
                "fade",
            ]
        )

    # if SCREEN_LOCK and read_template() == read_current_wall():
    #     return
    # storage_lockscreen()


if __name__ == "__main__":
    try:
        wall_start()
    except Exception as e:
        print(f"\n  Error: {e}")
