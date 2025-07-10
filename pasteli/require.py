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

import shutil,platform,os,warnings,subprocess
from . import utils,constants

if "PASTELI_SKIP_DEP_CHECK" in os.environ:
    pass
else:
    missing = False

    ds = utils.get_display_server()
    if shutil.which("xclip") == None and ds == constants.DS_X11:
        missing = "xclip"
        missApt = "xclip"
        missPac = "xclip"
        missDnf = "xclip"
        environment = "X11"
    if shutil.which("wl-paste") == None and ds == constants.DS_WAYLAND:
        missing = "wl-clipboard"
        missApt = "wl-clipboard"
        missPac = "wl-clipboard"
        missDnf = "wl-clipboard"
        environment = "Wayland"

    if missing:
        hasApt = not (not shutil.which("apt"))
        hasPac = not (not shutil.which("pacman"))
        hasDnf = not (not shutil.which("dnf"))
        if hasApt:
            install = f"sudo apt-get install {missApt}"
        elif hasPac:
            install = f"sudo pacman -S {missPac}"
        elif hasDnf:
            install = f"sudo dnf install {missDnf}"
        # if "PASTELI_INSTALL_DEPS" in os.environ:
        #     print(f"Installing missing dependencies... (pasteli requires `{missing}` to function on {environment}.)")
        #     import subprocess
        #     hasApt = not (not shutil.which("apt"))
        #     hasPac = not (not shutil.which("pacman"))
        #     hasDnf = not (not shutil.which("dnf"))
        #     if sum([hasApt,hasPac,hasDnf]) >= 2:
        #         raise RuntimeError("Cannot install packages automatically; multiple package managers present.")
        #     if hasApt:
        #         subprocess.run(["pkexec","apt-get","install","-y",missApt],check=True)
        #     if hasPac:
        #         subprocess.run(["pkexec","pacman","-S","--noconfirm",missPac],check=True)
        #     if hasDnf:
        #         subprocess.run(["pkexec","dnf","install","-y",missDnf],check=True)
        # else:
        misstext = f"PasteLi (a dependency) requires `{missing}` to function on {environment}."
        text = f"You are missing system dependencies! {misstext}"
        popup = f"You are missing system dependencies!\n{misstext}\n\nInstall with `{install}`"
        if shutil.which("kdialog"):
            subprocess.run(["kdialog","--error",popup])
        elif shutil.which("zenity"):
            subprocess.run(["zenity","--error","--text",popup])
        else:
            try:
                import tkinter as tk
                from tkinter import messagebox
                root = tk.Tk()
                root.withdraw()
                messagebox.showinfo("Error",popup)
            except ImportError as e:
                warnings.warn("Failed to show error popup!",ImportWarning)
        print(f"{install}\n\n")
        raise ImportError(text)