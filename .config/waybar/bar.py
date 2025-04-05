#!/usr/bin/env python

import re
import pathlib
import json
import argparse
import subprocess
import time


CONFIG_JSON = pathlib.Path(__file__).parent / "config.jsonc"
DIR_NAME_COLORSHEME = "theme"
TMP_FILE = pathlib.Path("/tmp/bar_toggle")


def enable_bar():
    if TMP_FILE.exists():
        TMP_FILE.unlink()
    subprocess.Popen(["waybar", "-c", str(CONFIG_JSON), "-s", str(read_jsonc())])


def disable_bar():
    TMP_FILE.write_text("disable")
    subprocess.Popen(["pkill", "-x", "waybar"])


def autostart():
    if TMP_FILE.exists():
        disable_bar()
    else:
        enable_bar()


def toggle():
    if TMP_FILE.exists():
        enable_bar()
    else:
        disable_bar()


def reload():
    subprocess.run(["pkill", "-x", "waybar"])
    subprocess.run(["waybar", "-c", str(CONFIG_JSON), "-s", str(read_jsonc())])


def read_json_without_comments():
    with open(CONFIG_JSON, "r") as f:
        jsonc_content = f.read()
        jsonc_content = re.sub(r"//.*", "", jsonc_content)
        jsonc_content = re.sub(r",\s*(]|})", r"\1", jsonc_content)
        data = json.loads(jsonc_content)
        return data


def read_jsonc():
    data = read_json_without_comments()
    result = pathlib.Path(__file__).parent / DIR_NAME_COLORSHEME / data["style-config"]
    return result


def current_style_css_name():
    data = read_json_without_comments()
    return data["style-config"]


def read_json_how_txt():
    with open(CONFIG_JSON, "r") as f:
        return f.read()


def replice_configure():
    if not args.theme:
        return None

    dir_path = CONFIG_JSON.parent / DIR_NAME_COLORSHEME
    theme_config_json = dir_path / args.theme / "config.json"

    if not theme_config_json.exists():
        raise FileNotFoundError(f"Config not found: {theme_config_json}")

    with open(CONFIG_JSON, "r") as f:
        base_config_lines = f.readlines()

    with open(theme_config_json, "r") as f:
        config_style_data = json.load(f)

    matched_keys = {}

    for line in base_config_lines:
        for k, v in config_style_data.items():
            pattern = rf'^\s*"{re.escape(k)}"\s*:'
            if re.search(pattern, line):
                matched_keys[k] = v

    return matched_keys if matched_keys else None


def set_theme():
    replacements = replice_configure()
    if not replacements:
        print("No matching keys to replace.")
        return

    with open(CONFIG_JSON, "r") as f:
        base_lines = f.readlines()

    new_lines = []
    for line in base_lines:
        replaced = False
        for key, value in replacements.items():
            pattern = rf'^(\s*"{re.escape(key)}"\s*:\s*)(.+?)(,?)\s*$'
            match = re.match(pattern, line)
            if match:
                new_value = json.dumps(value)
                line = f"{match.group(1)}{new_value}{match.group(3)}\n"
                replaced = True
                break
        new_lines.append(line)

    with open(CONFIG_JSON, "w") as f:
        f.writelines(new_lines)

    print("✔ Theme applied successfully!")


def main(args):
    if args.theme:
        dir_path = CONFIG_JSON.parent / DIR_NAME_COLORSHEME
        theme_path = dir_path / args.theme / "style.css"
        target_path = dir_path / current_style_css_name()
        try:
            set_theme()
        except:
            print(f"{args.theme}: not have `config.json`")
        target_path.write_text(theme_path.read_text())
    if args.enable:
        enable_bar()
    elif args.disable:
        disable_bar()
    elif args.autostart:
        autostart()
    elif args.toggle:
        toggle()
    elif args.reload:
        reload()
    elif args.theme is None:
        enable_bar()
        ...


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Starter Bar")
    parser.add_argument("theme", nargs="?", help="Theme name")
    parser.add_argument("-d", "--disable", action="store_true", help="Disable Bar")
    parser.add_argument("-e", "--enable", action="store_true", help="Enable Bar")
    parser.add_argument("-t", "--toggle", action="store_true", help="Toggle Bar")
    parser.add_argument("-a", "--autostart", action="store_true", help="Autostart Bar")
    parser.add_argument("-r", "--reload", action="store_true", help="Reload Bar")

    args, unknown = parser.parse_known_args()
    try:
        print(main(args))
    except KeyboardInterrupt:
        print("~ cancel ^^")
