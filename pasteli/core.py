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
from .utils import *
import subprocess
import warnings
import platform
import os
from urllib.parse import unquote_to_bytes
from . import errors
from typing import Optional, Union

if platform.system() == "windows" or os.name == "nt":
    # ALL OF THESE IMPORTS ARE ONLY FOR WINDOWS.
    # YEAH THATS RIGHT MICROSOFT YOU'RE A SPECIAL BOY!
    import win32clipboard as wc
    import win32con
    import struct

def copy_text_wl(text,encode="utf-8"):
    """
    Copies text to the clipboard, on Linux (Wayland).

    Args:
        text (str|bytes): The text to copy
        encode (str): The encoding that's being passed.
    """
    if encode != "bytes": text = text.encode(encode)
    # warnings.warn("pasteli.core.copy_text_wl(text,encode='utf-8') is not complete. Functionality may be missing.",errors.UnfinishedWarning)
    subprocess.run(["wl-copy"],input=text,check=True,close_fds=True)

def copy_text_x11(text,encode="utf-8"):
    """
    Copies text to the clipboard, on Linux (X11).

    Args:
        text (str|bytes): The text to copy
        encode (str): The encoding that's being passed.
    """
    if encode != "bytes": text = text.encode(encode)
    # warnings.warn("pasteli.core.copy_text_x11(text,encode='utf-8') is not complete. Functionality may be missing.",errors.UnfinishedWarning)
    subprocess.run(["xclip","-selection","clipboard"],input=text,check=True,close_fds=True)
    # raise NotImplementedError("pasteli.core.copy_text(text)")

def copy_text_windows(text,encode="utf-8"):
    """
    Copies text to the clipboard, on MacOS.

    Raises:
        WindowsError: Bytes were passed, or could not convert to UTF-16LE.

    Args:
        text (str|bytes): The text to copy
        encode (str): The encoding that's being passed.
    """
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
    """
    Copies text to the pasteboard, on MacOS.

    Args:
        text (str|bytes): The text to copy
        encode (str): The encoding that's being passed.
    """
    if encode != "bytes": text = text.encode(encode)
    subprocess.run(["pbcopy"],input=text,check=True,close_fds=True)
    # raise NotImplementedError("pasteli.core.copy_text_mac(text,encode='utf-8')")

def copy_file_wl(file,encode="utf-8"):
    """
    Copies a file to the clipboard, on Linux (Wayland).

    Args:
        file (str|bytes): The file path to copy
        encode (str): The encoding that's being passed.
    """
    raise NotImplementedError("pasteli.core.copy_file_wl(file,encode='utf-8')")

def copy_file_x11(files,encode="utf-8") -> None:
    """
    Copies a file to the clipboard, on Linux (X11).

    Args:
        files (list[str|bytes]): The file path to copy
        encode (str): The encoding that's being passed.
    """
    uris = [f"file://{os.path.abspath(file)}" for file in files if len(file) != 0]
    if encode != "bytes": uris = [uri.encode(encode) for uri in uris]
    uris = b"\n".join(uris)
    subprocess.run(["xclip","-selection","clipboard","-t","text/uri-list"],input=uris,check=True,close_fds=True)
    # '-t', 'text/uri-list'
    # raise NotImplementedError("pasteli.core.copy_file_x11(file,encode='utf-8')")

def copy_file_windows(file,encode="utf-8"):
    """
    Copies a file to the clipboard, on Windows.

    Args:
        file (str|bytes): The file path to copy
        encode (str): The encoding that's being passed.
    """
    raise NotImplementedError("pasteli.core.copy_file_windows(file,encode='utf-8')")

def copy_file_mac(file,encode="utf-8"):
    """
    Copies a file to the pasteboard, on MacOS.

    Args:
        file (str|bytes): The file path to copy
        encode (str): The encoding that's being passed.
    """
    raise NotImplementedError("pasteli.core.copy_file_mac(file,encode='utf-8')")

def paste_text_wl(decode="utf-8") -> Union[str,bytes]:
    """
    Pastes text from the clipboard, on Linux (Wayland).

    Args:
        decode (str): The encoding that will be returned
    
    Raises:
        TimeoutError: If a commandline utility takes too long to paste.
    
    Returns:
        str|bytes: The content pasted from the clipboard, according to the encoding.
    """
    try:
        value = subprocess.run(["wl-paste"],capture_output=True,check=True,timeout=5).stdout
        if value.endswith(b"\n"): value = value[:-1]
        if decode != "bytes": value = value.decode(decode)
        return value
    except subprocess.TimeoutExpired:
        raise TimeoutError("Wl-paste timed out, and the clipboard could not be pasted. (are you in a Wayland session?)")
    # raise NotImplementedError("pasteli.core.paste_text_wl(decode='utf-8')")

def paste_text_x11(decode="utf-8") -> Union[str,bytes]:
    """
    Pastes text from the clipboard, on Linux (X11).

    Args:
        decode (str): The encoding that will be returned
    
    Raises:
        TimeoutError: If a commandline utility takes too long to paste.
    
    Returns:
        str|bytes: The content pasted from the clipboard, according to the encoding.
    """
    try:
        # warnings.warn("pasteli.core.paste_text_x11(decode='utf-8') is not complete. Functionality may be missing.",errors.UnfinishedWarning)
        value = subprocess.run(["xclip","-selection","clipboard","-o"],capture_output=True,check=True,timeout=5).stdout
        if decode != "bytes": value = value.decode(decode)
        return value
    except subprocess.TimeoutExpired:
        raise TimeoutError("Xclip timed out, and the clipboard could not be pasted. (are you in an X11 session?)")

def paste_text_windows(decode="utf-8") -> Union[str,bytes]:
    """
    Pastes text from the clipboard, on Windows.

    Args:
        decode (str): The encoding that will be returned
    
    Raises:
        EncodingWarning: If the clipboard failed to paste due to being the wrong type of data. May also occur with no data.
    
    Returns:
        str|bytes: The content pasted from the clipboard, according to the encoding.
    """
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

def paste_text_mac(decode="utf-8") -> Union[str,bytes]:
    """
    Pastes text from the pasteboard, on MacOS.

    Args:
        decode (str): The encoding that will be returned
    
    Raises:
        TimeoutError: If a commandline utility takes too long to paste.
    
    Returns:
        str|bytes: The content pasted from the clipboard, according to the encoding.
    """
    try:
        value = subprocess.run(["pbpaste"],capture_output=True,check=True,timeout=5).stdout
        if value.endswith(b"\n"): value = value[:-1]
        if decode != "bytes": value = value.decode(decode)
        return value
    except subprocess.TimeoutExpired:
        raise TimeoutError("Pbpaste timed out, and the clipboard could not be pasted.")
    # raise NotImplementedError("pasteli.core.paste_text_wl(decode='utf-8')")

def paste_file_wl(decode="utf-8"):
    """
    Pastes a file from the clipboard, on Linux (Wayland).

    Args:
        decode (str): The encoding that will be returned
    
    Returns:
        str|bytes: A list of file paths from the clipboard, in the format of the encoding.
    """
    raise NotImplementedError("pasteli.core.paste_file_wl(decode='utf-8')")

def paste_file_x11(decode="utf-8"):
    """
    Pastes a file from the clipboard, on Linux (X11).

    Args:
        decode (str): The encoding that will be returned
    
    Raises:
        TimeoutError: If a commandline utility takes too long to paste.
    
    Returns:
        list[str|bytes]: A list of file paths from the clipboard, in the format of the encoding.
    """
    try:
        # warnings.warn("pasteli.core.paste_text_x11(decode='utf-8') is not complete. Functionality may be missing.",errors.UnfinishedWarning)
        raw = subprocess.run(["xclip","-selection","clipboard","-o","-t","text/uri-list"],capture_output=True,check=True,timeout=5).stdout
        uris = [x for x in raw.split(b"\r\n") if x != b""]
        value = []
        for uri in uris:
            parsed = uri.split(b"://")
            scheme = parsed[0]
            if scheme != b"file":
                warnings.warn(f"Not a file URL. ({uri} from {uris})",EncodingWarning)
                return []
            path = b"://".join(parsed[1:])
            value.append(unquote_to_bytes(path))
        if decode != "bytes": value = [x.decode(decode) for x in value]
        return value
    except subprocess.TimeoutExpired:
        raise TimeoutError("Xclip timed out, and the clipboard could not be pasted. (are you in an X11 session?)")
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            warnings.warn("Xclip returned exist status 1. Is the clipboard data a file or a list of files?",errors.ClipboardUtilityWarning)
    # raise NotImplementedError("pasteli.core.paste_file_x11(decode='utf-8')")

def copy_text(text,encoding="utf-8"):
    """
    Calls the individual copying function for the active display server.

    Args:
        text (str or bytes): The text to copy
        encoding (str): The encoding of the value you're passing
    
    Raises:
        OSError: Unsupported system
        OSError: Could not determine system
        WindowsError: Bytes were passed, or could not convert to UTF-16LE.
    
    Returns:
        None
    """
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
            raise KeyError("pasteli.utils.get_display_server() returned unexpected value.")

def copy_file(file,encoding="utf-8"):
    """
    Calls the individual copying function for the active display server.

    Args:
        file (str or bytes): The file path to copy
        encoding (str): The encoding of the value you're passing
    
    Raises:
        OSError: Unsupported system
        OSError: Could not determine system
        WindowsError: Bytes were passed, or could not convert to UTF-16LE.
    
    Returns:
        None
    """
    ds = get_display_server()
    match ds:
        case const.DS_WAYLAND:
            return copy_file_wl(file,encode=encoding)
        case const.DS_X11:
            return copy_file_x11(file,encode=encoding)
        case const.DS_WINDOWS:
            return copy_file_windows(file,encode=encoding)
        case const.DS_WINDOWSERVER:
            return copy_file_mac(file,encode=encoding)
        case _:
            raise KeyError("pasteli.utils.get_display_server() returned unexpected value.")

def paste_text(encoding="utf-8") -> Union[str,bytes]:
    """
    Calls the individual pasting function for the active display server.

    Args:
        encoding (str): The encoding that will be returned
    
    Raises:
        TimeoutError: If a commandline utility takes too long to paste.
        KeyError: If pasteli.utils.get_display_server() returned an unexpected value.
        EncodingWarning: If the clipboard failed to paste due to being the wrong type of data. May also occur with no data.
        OSError: Unsupported system
        OSError: Could not determine system
    
    Returns:
        str|bytes: The content pasted from the clipboard, according to the encoding.
    """
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
            raise KeyError("pasteli.utils.get_display_server() returned unexpected value.")

def paste_file(encoding="utf-8") -> Union[str,bytes]:
    """
    Calls the individual pasting function for the active display server.

    Args:
        encoding (str): The encoding that will be returned
    
    Raises:
        TimeoutError: If a commandline utility takes too long to paste.
        KeyError: If pasteli.utils.get_display_server() returned an unexpected value.
        EncodingWarning: If the clipboard failed to paste due to being the wrong type of data. May also occur with no data.
        OSError: Unsupported system
        OSError: Could not determine system
    
    Returns:
        str|bytes: The content pasted from the clipboard, according to the encoding.
    """
    ds = get_display_server()
    match ds:
        case const.DS_WAYLAND:
            return paste_file_wl(decode=encoding)
        case const.DS_X11:
            return paste_file_x11(decode=encoding)
        case const.DS_WINDOWS:
            return paste_file_windows(decode=encoding)
        case const.DS_WINDOWSERVER:
            return paste_file_mac(decode=encoding)
        case _:
            raise KeyError("pasteli.utils.get_display_server() returned unexpected value.")

def copy(mode:int,text:Optional[Union[str,bytes]]=None,file:Optional[Union[str,bytes]]=None,encoding:str="utf-8") -> None:
    """
    Calls the individual copying function for the type (`mode`) of medium supplied.
    Pass one of (text, file)

    Args:
        mode (int): What type of medium? Use `pasteli.constants.CMODE_*` values.
        text (str or bytes): The data to copy (works for all modes)
        file (str or bytes, optional): The file path to copy (works for CMODE_FILE)
        encoding (str): The encoding of the value you're passing (works for CMODE_TEXT, CMODE_FILE)
    
    Raises:
        TypeError: If no data is passed
        KeyError: If no valid mode is passed.
        OSError: Unsupported system
        OSError: Could not determine system
        WindowsError: Bytes were passed, or could not convert to UTF-16LE.
    
    Returns:
        None
    """

    if text == None and file == None:
        raise TypeError("Pass exactly one of (text, file)")

    match mode:
        case const.CMODE_TEXT:
            return copy_text(text,encoding=encoding)
        case const.CMODE_FILE:
            return copy_file(file or text,encoding=encoding)
        case _:
            raise KeyError("copy(mode, ...)    mode should be a CMODE constant from pasteli.constants.")

def paste(mode:int,encoding:str="utf-8") -> Union[str,bytes]:
    """
    Calls the individual pasting function for the type (`mode`) of medium supplied.

    Args:
        mode (int): What type of medium? Use pasteli.constants.CMODE_* values here.
        encoding (str): The encoding that will be returned
    
    Raises:
        TimeoutError: If a commandline utility takes too long to paste.
        KeyError: If no valid mode is passed.
        EncodingWarning: If the clipboard failed to paste due to being the wrong type of data. May also occur with no data.
        OSError: Unsupported system
        OSError: Could not determine system
    
    Returns:
        str|bytes: The content pasted from the clipboard, according to the encoding.
    """
    match mode:
        case const.CMODE_TEXT:
            return paste_text(encoding=encoding)
        case const.CMODE_FILE:
            return paste_file(encoding=encoding)
        case _:
            raise KeyError("paste(mode)    mode should be a CMODE constant from pasteli.constants.")