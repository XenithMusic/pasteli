"""
PasteLi is a Python library that handles clipboard operations.
Copyright (C) 2025 cookiiq <xenith.contact.mail@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os,platform
from . import constants as const

def get_display_server() -> int:
    """
    Returns the active display server as a `pasteli.constants.DS_*` value.

    Raises:
        OSError: Could not determine display server.
        OSError: Jython does not work on MacOS and Windows.
        OSError: Unsupported Operating System.
        OSError: No display server found.
    
    Returns:
        int: A `pasteli.constants.DS_*` value representing the active display server.
    """
    if os.environ.get("WAYLAND_DISPLAY"):
        return const.DS_WAYLAND
    elif os.environ.get("DISPLAY"):
        return const.DS_X11
    else:
        match platform.system():
            case "Windows":
                return const.DS_EXPLORER
            case "Darwin":
                return const.DS_WINDOWSERVER
            case "Linux":
                raise OSError("No wayland or X11 session found. ($WAYLAND_DISPLAY and $DISPLAY not set.)")
            case "iOS":
                raise OSError("iOS is not supported.")
            case "iPadOS":
                raise OSError("iPadOS is not supported.")
            case "Android":
                raise OSError("Android is not supported.")
            case "Java":
                raise OSError("Cannot determine Display Servers other than Linux (Wayland) and Linux (X11) when using Jython.")
            case _:
                raise OSError("Could not determine your operating system.")