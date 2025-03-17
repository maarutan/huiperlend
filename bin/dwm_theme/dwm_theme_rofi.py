#!/usr/bin/env python3

import pathlib
import os
import subprocess
from typing import Optional

HOME = pathlib.Path.home()
DWM_CONFIG = HOME / ".config" / "dwm" / "source"
THEME_DIR = DWM_CONFIG / "config" / "themes"
CACHE_THEME = HOME / ".cache" / "current_theme"
SYSTEM_THEME = HOME / ".cache" / "system_theme"
ROFI_THEME = pathlib.Path(__file__).parent / ".assets" / "rofi_theme" / "theme.rasi"
ICON_DIR = pathlib.Path(__file__).parent / ".assets" / "photo"


def get_themes() -> list:
    try:
        return sorted(
            [i for i in os.listdir(THEME_DIR) if os.path.isdir(THEME_DIR / i)]
        )
    except Exception as e:
        print(f"Ошибка при получении списка тем: {e}")
        return []


def get_icon_for_theme(theme: str) -> str:
    for ext in ["png", "jpg", "jpeg", "svg", "ico", "bmp", "gif", "webp"]:
        icon_path = ICON_DIR / f"{theme}.{ext}"
        if icon_path.exists():
            return str(icon_path)
    return ""


def choose_theme() -> Optional[str]:
    themes = get_themes()
    if not themes:
        print("Нет доступных тем.")
        return None

    array = []
    for theme in themes:
        icon_path = get_icon_for_theme(theme)
        array.append(f"{theme}\x00icon\x1f{icon_path}")

    process = subprocess.run(
        ["rofi", "-dmenu", "-theme", str(ROFI_THEME), "-p", "Выберите тему"],
        input="\n".join(array),
        text=True,
        capture_output=True,
    )

    theme = process.stdout.strip()
    return theme if theme in themes else None


def choose_variant(theme: str) -> Optional[str]:
    variants = {"1": "dark", "2": "light"}

    array = []
    for key, name in variants.items():
        icon_path = get_icon_for_theme(
            f"{theme}_{key}"
        )  # Ищем иконки gruvbox_1.png, gruvbox_2.png
        array.append(f"{name}\x00icon\x1f{icon_path}")

    process = subprocess.run(
        ["rofi", "-dmenu", "-theme", str(ROFI_THEME), "-p", "Выберите вариант"],
        input="\n".join(array),
        text=True,
        capture_output=True,
    )

    choice = process.stdout.strip().split(" ")[0]  # Берём только "1" или "2"
    return choice if choice in variants else None


def read_theme_file(theme: str, variant: str) -> str:
    """Читает файл с конфигурацией темы (1 или 2)."""
    file_path = THEME_DIR / theme / variant
    if not file_path.exists():
        print(f"Файл {file_path} не найден!")
        return ""

    with open(file_path, "r") as f:
        return f.read().strip()


def write_current_theme(theme: str):
    try:
        with open(CACHE_THEME, "w") as f:
            f.write(theme)
        print(f"Выбрана тема: {theme}")
    except Exception as e:
        print(f"Ошибка при записи темы: {e}")


def write_system_theme(content: str):
    """Записывает выбранный вариант (1/2) в системный кэш."""
    try:
        with open(SYSTEM_THEME, "w") as f:
            f.write(content)
        print(f"Системная тема установлена: {content}")
    except Exception as e:
        print(f"Ошибка при записи системной темы: {e}")


def apply_theme(theme: str, variant: str):
    """Применяет тему и выполняет скрипты настройки."""
    content = read_theme_file(theme, variant)
    if not content:
        return

    write_system_theme(variant)

    with open(DWM_CONFIG / "config" / "themes" / "theme.h", "w") as f:
        f.write(content)

    print(f"✔ Обновлен theme.h [{variant}]")

    scripts = [
        "$HOME/.config/dunst/.scrips/source.py",
        "$HOME/.config/kitty/.scrips/theme.py",
        "$HOME/.config/rofi/.scrips/theme.py",
    ]
    for script in scripts:
        subprocess.Popen(script, shell=True)

    print("✔ Применены изменения.")


def main():
    theme = choose_theme()
    if not theme:
        print("Тема не выбрана.")
        return

    write_current_theme(theme)

    variant = choose_variant(theme)
    if not variant:
        print("Вариант темы не выбран.")
        return

    apply_theme(theme, variant)


if __name__ == "__main__":
    main()
