#!/usr/bin/env python3

# zprogfetch.py
# github: https://github.com/maarutan
# (c) by maaru.tan

import os
import subprocess
import sys

# DONE: ---=== Global Vars ===---

user = os.getenv("USER", "unknown")
hostname = os.uname().nodename
shell = os.path.basename(os.getenv("SHELL", "unknown"))
distro = subprocess.run(
    ". /etc/os-release && echo $ID", shell=True, text=True, capture_output=True
).stdout.strip()
kernel = (
    subprocess.run("uname -r", shell=True, text=True, capture_output=True)
    .stdout.split("-")[0]
    .strip()
)
ram_usage = subprocess.run(
    "free -t | awk 'NR == 2 {printf(\"%.2f%%\", $3/$2*100)}'",
    shell=True,
    text=True,
    capture_output=True,
).stdout.strip()


wm = "unknown"
try:
    wm_id = subprocess.run(
        "xprop -root -notype | awk '$1==\"_NET_SUPPORTING_WM_CHECK:\"{print $5}'",
        shell=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    if wm_id:
        wm = subprocess.run(
            f"xprop -id {wm_id} -notype -f _NET_WM_NAME 8t | grep 'WM_NAME' | cut -f2 -d '\"'",
            shell=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
except Exception:
    pass


white = "\033[37m"
cyan = "\033[36m"
blue = "\033[34m"
green = "\033[32m"
purple = "\033[35m"
bold = "\033[1m"
end = "\033[0m"

# DONE: ---=== ui  ===---


def repeat_by_len(text: str, char: str) -> str:
    return char * len(text)


output = f"""
{bold}{blue}           ██           {end}{bold}{blue}{user}{cyan}@{purple}{hostname}{end}
{bold}{blue}          ████          {end}{green}{repeat_by_len(f"{user}@{hostname}", "─")}
{bold}{blue}          ▀████         {end}
{bold}{blue}        ██▄ ████        {end}{bold}{purple}  {blue}os {green}  {cyan}{distro}{end}
{bold}{blue}       ██████████       {end}{bold}{purple}  {blue}sh {green}  {cyan}{shell}{end}
{bold}{blue}      ████▀  ▀████      {end}{bold}{purple}  {blue}wm {green}  {cyan}{wm}{end}
{bold}{blue}     ████▀    ▀████     {end}{bold}{purple}  {blue}kr {green}  {cyan}{kernel}{end}
{bold}{blue}    ▀▀▀          ▀▀▀    {end}{bold}{purple}  {blue}ram {green} {cyan}{ram_usage}{end}

"""


sys.stdout.write(output)
