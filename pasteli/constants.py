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

import sys,subprocess

# Internals

VERSION = "0.1.0"
PY_IMPLEMENTATION = sys.implementation.name.capitalize()
PY_VERSION = ".".join([str(x) for x in sys.version_info[:3]])

# Copy Modes

CMODE_TEXT = 1

# Display Servers (actually just used for the system that handles the clipboard)

DS_WINDOWS = 1           # Windows - Requires kernel, hense why it's not DS_EXPLORER.
DS_EXPLORER = DS_WINDOWS #         - alias for DS_WINDOWS
DS_WINDOWSERVER = 2      # MacOS   - pbcopy, pbpaste
DS_X11 = 3               # Linux   - xclip
DS_WAYLAND = 4           #         - wl-copy, wl-paste\