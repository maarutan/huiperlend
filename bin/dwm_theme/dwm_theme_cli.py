#!/usr/bin/env python3

import pathlib, os, argparse, sys, subprocess

HOME = pathlib.Path.home()
DWM_CONFIG = HOME / ".config" / "dwm" / "source"
THEME_FILE = HOME / ".config" / "dwm" / "source" / "config" / "themes" / "theme.h"
THEME_DIR = HOME / ".config" / "dwm" / "source" / "config" / "themes"
SYSTEM_THEME = HOME / ".cache" / "system_theme"
CACHE_THEME = HOME / ".cache" / "current_theme"


def run():
    runner(
        "$HOME/.config/dunst/.scrips/source.py",
        "$HOME/.config/kitty/.scrips/theme.py",
        "$HOME/.config/rofi/.scrips/theme.py",
    )


def read_system_theme() -> str:
    with open(SYSTEM_THEME, "r") as f:
        return f.read().strip()


def write_system_theme(content: str) -> None:
    with open(SYSTEM_THEME, "w") as f:
        f.write(content)


def runner(*command, null=False, pkill=False) -> None:
    if not command:
        return

    blacklist = [
        "rm",
        "poweroff",
        "shutdown",
        "reboot",
        "dd",
        "mkfs",
    ]

    for cmd in command:
        first_word = cmd.split()[0] if cmd else ""

        if first_word in blacklist:
            print(f"Erorr: {first_word} is blacklisted!")
            continue

        if null:
            subprocess.Popen(cmd + " >/dev/null 2>&1", shell=True)
        else:
            subprocess.Popen(cmd, shell=True)


def get_theme() -> list:
    try:
        return [
            i
            for i in os.listdir(THEME_DIR)
            if os.path.isdir(os.path.join(THEME_DIR, i))
        ]
    except Exception as e:
        print(f"Get theme error: {e}")
        return []


def get_inset_theme(content: str) -> list:
    try:
        theme_path = THEME_DIR / content
        if not theme_path.is_dir():
            print(f"Error: theme '{content}' not found.")
            return []
        return sorted(
            [
                file
                for file in os.listdir(theme_path)
                if os.path.isfile(theme_path / file)
            ]
        )
    except Exception as e:
        print(f"Error getting inset theme: {e}")
        return []


def read_theme_file(theme: str, filename: str) -> str:
    with open(THEME_DIR / theme / filename, "r") as f:
        return f.read().strip()


def write_current_theme(content: str):
    with open(CACHE_THEME, "w") as f:
        f.write(content)


def write_theme_file_content(theme: str, filename: str, content: str) -> None:
    with open(THEME_DIR / theme / filename, "w") as f:
        f.write(content)


parser = argparse.ArgumentParser(description="dwm theme")

parser.add_argument("name", nargs="?", type=str, help="theme name or index")
parser.add_argument("-l", "--list", action="store_true", help="list available themes")
parser.add_argument(
    "-s", "--set", metavar="variant", type=str, help="set a theme variant"
)

args = parser.parse_args()

if args.name:
    themes = get_theme()
    try:
        theme_index = int(args.name) - 1
        if 0 <= theme_index < len(themes):
            theme_name = themes[theme_index]
        else:
            print(f"Error: theme index '{args.name}' out of range.")
            sys.exit(1)
    except ValueError:
        if args.name in themes:
            theme_name = args.name
        else:
            print(f"Error: theme '{args.name}' not found.")
            sys.exit(1)

    theme_index = themes.index(theme_name) + 1
    sub_themes = get_inset_theme(theme_name)

    theme_mapping = {"1": "dark", "2": "light"}

    available_subthemes = [theme_mapping.get(t, t) for t in sub_themes]

    print(f"\nTheme name: [ {theme_index}. {theme_name} ]\n")
    write_current_theme(theme_name)

    print("1 = dark\n2 = light\n--------------------")
    if args.set:
        selected_variant = theme_mapping.get(args.set, args.set)

        if selected_variant in available_subthemes:
            content = read_theme_file(theme_name, args.set)
            write_system_theme("dark" if selected_variant == "dark" else "light")
            print(f"✔ System theme set to {selected_variant}")
            write_theme_file_content("./", "theme.h", content)
            print(f"✔ Updated theme.h [{read_system_theme()}]")
            run()
            sys.exit(0)
        else:
            print(f"Error: theme variant '{args.set}' not found in '{theme_name}'.")
            sys.exit(1)

elif args.list:
    themes = get_theme()
    if themes:
        print("\nAvailable themes:")
        print("\n".join(f"   {j}. {i}" for j, i in enumerate(themes, 1)))
    else:
        print("No themes found.")
