#!/usr/bin/env python3

# push dotfiles
# https://github.com/maaru/dotfiles.git
# Copyright (c) 2025 maarutan \ Marat Arzymatov. All Rights Reserved.

from logic.logic import *
# DONE: ------=== Global Repozitory  ===------

global_repo_json(
    dirname="dotfiles",
    url="https://github.com/maarutan/dotfiles",
    branch="main",
    # ------------------------------------------
    push_object={
        ".config": {
            "kitty": f"{HOME}/.config/kitty",
            "zsh": f"{HOME}/.config/zsh",
            "btop": f"{HOME}/.config/btop",
            "nvim": f"{HOME}/.config/nvim",
            "dwm": f"{HOME}/.config/dwm",
            "fastfetch": f"{HOME}/.config/fastfetch",
            "gtk-2.0": f"{HOME}/.config/gtk-2.0",
            "gtk-3.0": f"{HOME}/.config/gtk-3.0",
            "neofetch": f"{HOME}/.config/neofetch",
            "rofi": f"{HOME}/.config/rofi",
            "picom": f"{HOME}/.config/picom",
            "qt5ct": f"{HOME}/.config/qt5ct",
            "qt6ct": f"{HOME}/.config/qt6ct",
            "yay": f"{HOME}/.config/yay",
            "yazi": f"{HOME}/.config/yazi",
            "dunst": f"{HOME}/.config/dunst",
            "cava": f"{HOME}/.config/cava",
            "flameshot": f"{HOME}/.config/flameshot",
            "xsettingsd": f"{HOME}/.config/xsettingsd",
            "mimeapps.list": f"{HOME}/.config/mimeapps.list",
            "user-dirs.dirs": f"{HOME}/.config/user-dirs.dirs",
            "user-dirs.locale": f"{HOME}/.config/user-dirs.locale",
        },
        # -------------
        ".local": {
            "bin": f"{HOME}/.local/bin",
            "plank_themes": f"{HOME}/.local/share/plank",
        },
        # -------------
        ".themes": f"{HOME}/.themes",
        # -------------
        "Pictures": {
            "mcrfScins": f"{HOME}/Pictures/mcrfScins",
            "profile": f"{HOME}/Pictures/profile",
            "screenshots": f"{HOME}/Pictures/screenshots",
            "wallpapers": f"{HOME}/Pictures/wallpapers",
        },
        # -------------
        "Videos": f"{HOME}/Videos",
        ".p10k.zsh": f"{HOME}/.p10k.zsh",
        ".viebrc": f"{HOME}/.viebrc",
        ".Xauthority": f"{HOME}/.Xauthority",
        ".xinitrc": f"{HOME}/.xinitrc",
        ".zshrc": f"{HOME}/.zshrc",
        ".Xresources": f"{HOME}/.Xresources",
    },
)

# INFO: ------=== Push More ===------

push_more_json(
    {
        "dirname": "push_zsh_zinit",
        "url": "https://github.com/maarutan/zinit",
        "branch": "main",
        # ------------------------------------------
        "push_object": {},
    },
)
