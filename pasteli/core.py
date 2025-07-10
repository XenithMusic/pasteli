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

from . import constants as const
import subprocess
import warnings
import platform
import os
from . import errors

if platform.system() == "windows" or os.name == "nt":
    # ALL OF THESE ARE ONLY FOR WINDOWS.
    # YEAH THATS RIGHT MICROSOFT YOU'RE A SPECIAL BOY!
    import win32clipboard as wc
    import win32con
    import struct

def copy_text_wl(text,encode="utf-8"):
    if encode != "bytes": text = text.encode(encode)
    # warnings.warn("pasteli.core.copy_text_wl(text,encode='utf-8') is not complete. Functionality may be missing.",errors.UnfinishedWarning)
    subprocess.run(["wl-copy"],input=text,check=True,close_fds=True)

def copy_text_x11(text,encode="utf-8"):
    if encode != "bytes": text = text.encode(encode)
    # warnings.warn("pasteli.core.copy_text_x11(text,encode='utf-8') is not complete. Functionality may be missing.",errors.UnfinishedWarning)
    subprocess.run(["xclip","-selection","clipboard"],input=text,check=True,close_fds=True)
    # raise NotImplementedError("pasteli.core.copy_text(text)")

def copy_text_windows(text,encode="utf-8"):
    if encode == "bytes": raise WindowsError("Cannot reliably convert from bytes.")
    try:
        if encode != "utf-16le": text = text.encode("utf-16le")
    except UnicodeDecodeError as e:
        raise WindowsError("Could not convert to UTF-16LE, which is necessary because windows is a special boy.")
    wc.OpenClipboard()
    wc.EmptyClipboard()
    wc.SetClipboardData(win32con.CF_UNICODETEXT,text)
    wc.CloseClipboard()

def copy_text_mac(text,encode="utf-8"):
    if encode != "bytes": text = text.encode(encode)
    subprocess.run(["pbcopy"],input=text,check=True,close_fds=True)
    # raise NotImplementedError("pasteli.core.copy_text_mac(text,encode='utf-8')")

def paste_text_wl(decode="utf-8"):
    try:
        value = subprocess.run(["wl-paste"],capture_output=True,check=True,timeout=5).stdout
        if value.endswith(b"\n"): value = value[:-1]
        if decode != "bytes": value = value.decode(decode)
        return value
    except subprocess.TimeoutExpired:
        raise TimeoutError("Xclip timed out, and the clipboard could not be pasted. (are you in an X11 session?)")
    # raise NotImplementedError("pasteli.core.paste_text_wl(decode='utf-8')")

def paste_text_x11(decode="utf-8"):
    try:
        # warnings.warn("pasteli.core.paste_text_x11(decode='utf-8') is not complete. Functionality may be missing.",errors.UnfinishedWarning)
        value = subprocess.run(["xclip","-selection","clipboard","-o"],capture_output=True,check=True,timeout=5).stdout
        if decode != "bytes": value = value.decode(decode)
        return value
    except subprocess.TimeoutExpired:
        raise TimeoutError("Xclip timed out, and the clipboard could not be pasted. (are you in an X11 session?)")

def paste_text_windows(decode="utf-8"):
    wc.OpenClipboard()
    try:
        data = wc.GetClipboardData(win32con.CF_UNICODETEXT)
    except TypeError:
        data = None
        warnings.warn("Clipboard doesn't contain text data.",EncodingWarning)
    finally:
        wc.CloseClipboard()
    return data
    # raise NotImplementedError("pasteli.core.paste_text_windows(decode='utf-8')")

def paste_text_mac(decode="utf-8"):
    try:
        value = subprocess.run(["pbpaste"],capture_output=True,check=True,timeout=5).stdout
        if value.endswith(b"\n"): value = value[:-1]
        if decode != "bytes": value = value.decode(decode)
        return value
    except subprocess.TimeoutExpired:
        raise TimeoutError("Xclip timed out, and the clipboard could not be pasted. (are you in an X11 session?)")
    # raise NotImplementedError("pasteli.core.paste_text_wl(decode='utf-8')")

def get_display_server() -> int:
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
            case _:
                raise OSError("Could not determine your operating system.")

def copy_text(text,encoding="utf-8"):
    ds = get_display_server()
    match ds:
        case const.DS_WAYLAND:
            return copy_text_wl(text,encode=encoding)
        case const.DS_X11:
            return copy_text_x11(text,encode=encoding)
        case const.DS_WINDOWS:
            return copy_text_windows(text,encode=encoding)
        case const.DS_WINDOWSERVER:
            return copy_text_mac(text,encode=encoding)
        case _:
            raise KeyError("pasteli.core.get_display_server() returned unexpected value.")

def paste_text(encoding="utf-8"):
    ds = get_display_server()
    match ds:
        case const.DS_WAYLAND:
            return paste_text_wl(decode=encoding)
        case const.DS_X11:
            return paste_text_x11(decode=encoding)
        case const.DS_WINDOWS:
            return paste_text_windows(decode=encoding)
        case const.DS_WINDOWSERVER:
            return paste_text_mac(decode=encoding)
        case _:
            raise KeyError("pasteli.core.get_display_server() returned unexpected value.")

def copy(mode,text=None,encoding="utf-8"):
    """
    DESCRIPTION: Calls the individual copying function for the type (`mode`) of medium supplied.
    ARGUMENT: mode = What type of medium? Use pasteli.constants.CMODE_* values here.
    ARGUMENT: text = The text to copy (CMODE_TEXT)
    """
    match mode:
        case const.CMODE_TEXT:
            return copy_text(text,encoding=encoding)
        case _:
            raise KeyError("copy(mode, ...)    mode should be a CMODE constant from pasteli.constants.")

def paste(mode,encoding="utf-8"):
    """
    DESCRIPTION: Calls the individual pasting function for the type (`mode`) of medium supplied.
    ARGUMENT: mode = What type of medium? Use pasteli.constants.CMODE_* values here.
    """
    match mode:
        case const.CMODE_TEXT:
            return paste_text(encoding=encoding)
        case _:
            raise KeyError("paste(mode)    mode should be a CMODE constant from pasteli.constants.")