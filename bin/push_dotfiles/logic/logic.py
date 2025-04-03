#!/usr/bin/env python3

# push dotfiles \ logic file
# https://github.com/maaru/dotfiles.git
# Copyright (c) 2025 maarutan \ Marat Arzymatov. All Rights Reserved.

# DONE: ------=== Imports ===------
import os
import subprocess
import random
import shutil
import sys
import pathlib
import json
import time

# DONE: ------=== Variables ===------

DEBUG = False
HOME = pathlib.Path.home()
RESULT_DIR = pathlib.Path(__file__).parent.parent / "dist"
JSON_NAME = "dotbase.json"

# INFO: for git
GIT_CLONE = "git clone --depth 1"
GIT_PULL = "git pull"
GIT_PUSH = "git push"

# INFO: for reset local repo to remote
GIT_CLEAN = "git clean -fdx"
GIT_RESET = "git reset --hard origin/$(git rev-parse --abbrev-ref HEAD)"
GIT_FETCH = "git fetch --all"

# INFO : colors for print
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
YELLOW = "\033[93m"
PURPLE = "\033[95m"
AUQA = "\033[96m"


# DONE: ------=== Functions ===------


def shell(command) -> str | None:
    blacklist = [
        "poweroff",
        "reboot",
        "rm",
        "shutdown",
    ]
    if command.split()[0] in blacklist:
        return print(f"skipping: {command}")
    else:
        return subprocess.run(
            command,
            shell=True,
            text=True,
            capture_output=True,
        ).stdout.strip()


def global_repo_json(dirname: str, url: str, branch: str, push_object: dict) -> None:
    json_path = pathlib.Path(__file__).parent.parent / JSON_NAME

    if json_path.exists():
        with open(json_path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    data["dotfiles"] = {
        "dirname": dirname,
        "url": url,
        "branch": branch,
        "push_object": push_object,
    }

    if "push_more" in data and not data["push_more"]:
        del data["push_more"]

    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)


def push_more_json(*repos):
    json_path = pathlib.Path(__file__).parent.parent / JSON_NAME

    if json_path.exists():
        with open(json_path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    if not repos:
        if "push_more" in data:
            del data["push_more"]
    else:
        data["push_more"] = {}
        existing_urls = set()

        for repo in repos:
            if isinstance(repo, dict) and all(
                k in repo for k in ["dirname", "url", "branch"]
            ):
                if repo["url"] not in existing_urls:
                    new_index = str(len(data["push_more"]) + 1)
                    data["push_more"][new_index] = repo
                    existing_urls.add(repo["url"])
                else:
                    if DEBUG:
                        print(f"⚠️  Repository {repo['url']} already exists, skipped")
            else:
                print(f"Error: Invalid format for {repo}")

    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)


def read_json() -> dict:
    json_path = pathlib.Path(__file__).parent.parent / JSON_NAME

    if not json_path.exists():
        print(f"  File {JSON_NAME} not found, returning empty dict.")
        return {}

    try:
        with open(json_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {JSON_NAME} is not a valid JSON file.")
        return {}


class get_json:
    def __init__(self, read_json) -> None:
        self.read_json = read_json

    def get_url(self, name):
        self.read_json if self.read_json else None
        return self.read_json[name]["url"]

    def get_branch(self, name):
        self.read_json if self.read_json else None
        return self.read_json[name]["branch"]

    def get_push_object(self, name):
        self.read_json if self.read_json else None
        return self.read_json[name]["push_object"]

    def get_dirname(self, name: str) -> str:
        self.read_json if self.read_json else None
        return self.read_json[name]["dirname"]

    def __str__(self) -> str:
        return str(self.read_json)


def check_dir(path):
    if not pathlib.Path(path).exists():
        shell(f"mkdir -p {path}")
    elif DEBUG:  # pragma: no cover
        print(f"Directory {path} already exists.")


def repo_exists(url: str) -> bool:
    env = os.environ.copy()
    env["GIT_ASKPASS"] = "true"
    env["GIT_TERMINAL_PROMPT"] = "0"

    result = subprocess.run(
        ["git", "ls-remote", "--exit-code", url],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    return result.returncode == 0


def check_dot_git(path, name):
    path = pathlib.Path(path)
    json_data = get_json(read_json())
    dirname = json_data.get_dirname(name)
    repo_url = json_data.get_url(name)
    branch = json_data.get_branch(name)

    if not (path / ".git").exists():
        print(f"\n{RED} => ERROR: {YELLOW}Checking repository: {repo_url}{RESET} ")

        if repo_exists(repo_url):
            print(f"✅ Cloning {repo_url} into {path}")
            shell(f"{GIT_CLONE} {repo_url} {path}")
        else:
            print(
                f"{PURPLE} -> Repository {repo_url} does not exist, initializing empty repo. {RESET}\n\n"
            )
            time.sleep(0.2)
            print(f"{GREEN} ~~ INFO:{RESET} created dir in: {PURPLE}{path}{RESET}")
            time.sleep(0.2)
            print(f"{GREEN} ~~ INFO:{RESET} created branch: {PURPLE}{branch}{RESET}")
            time.sleep(0.2)
            print(f"{GREEN} ~~ INFO:{RESET} ---=== {PURPLE}{dirname}{RESET} ===---\n")

            shell(f"git init -b {branch} {path}")
            return "not exists repo"
    else:
        print(".git already exists")
        return "exits .git"


def copy_item(push_object):
    dict_keys = []
    dirs = []
    files = []

    for key, value in push_object.items():
        if isinstance(value, dict):
            dict_keys.append(key)
        elif isinstance(value, str):
            p = pathlib.Path(value)
            if p.is_dir():
                dirs.append(key)
            elif p.is_file():
                files.append(key)
            else:
                print(f"Unknown or non-existent path for '{key}': {value}")
        else:
            print(f"Skipping '{key}' (type {type(value)})")

    for k in dict_keys:
        print(f"  dir: {k}")
    for d in dirs:
        print(f"  dir: {d}")
    for f in files:
        print(f"  file: {f}")


# def prepare_push():
#     myjson = get_json(read_json())
#     name = "dotfiles"
#     dirname = myjson.get_dirname(name)
#     dirname = RESULT_DIR / dirname
#     check_dir_git = check_dot_git(dirname, name)
#
#     if check_dir_git == "not exists repo":
#
#     elif check_dir_git == "exits .git":


# prepare_push()


def main():
    data = get_json(read_json())
    name = "dotfiles"
    path = RESULT_DIR / data.get_dirname(name)
    push_object = data.get_push_object(name)
    copy_item(push_object)
    # print(data.get_push_object(name))


main()
