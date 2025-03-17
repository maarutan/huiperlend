#!/usr/bin/env python3

"""
you need to install screeninfo
    `pipx install screeninfo`

or

    `yay -S python-screeninfo`
"""

from screeninfo import get_monitors


def get_display():
    for monitor in get_monitors():
        return f"{monitor.width}x{monitor.height}"


if __name__ == "__main__":
    print(get_display())
