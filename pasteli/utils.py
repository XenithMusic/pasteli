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