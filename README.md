# Pasteli

Pasteli is a cross-platform python library that allows developers to easily access the clipboard, allowing copy and paste of both text and non-text items.

> [!IMPORTANT]
> Pasteli is in active development, and may not have complete support for all features on all platforms.

## Operating System Support

|Legend|
|------|
|✅ = Working|
|☑️ = Partially Working|
|❌ = Not Working|
|➖ = Not Planned|

|Operating System|Windowing System|Supported|Notes     |
|----------------|----------------|---------|----------|
|Windows         |N/A             |☑️|Windows support may be inconsistent.|
|MacOS           |N/A             |☑️||
|Linux           |X11             |✅||
|Linux           |Wayland         |✅||
|iOS             |N/A             |➖|
|iPadOS          |N/A             |➖|
|Android         |N/A             |➖|

> [!WARNING]
> Pasteli may also have problems running on Jython, because `platform.system()` returns `"Java"` on the Jython interpreter, which is used to determine Windows and MacOS operations.

## Clipboard Support

|Type     |Copy Support|Paste Support|Notes           |
|---------|------------|-------------|----------------|
|Text             |✅|✅||
|Text (with MIME) |❌|❌||
|Rich Text        |❌|❌||
|Raw Images       |❌|❌||
|Files            |☑️|☑️|Only implemented on X11 and Wayland|
|Raw Audio        |➖|➖||
|Raw Video        |➖|➖||

## Installation

Pasteli is not currently on PyPI, however you can use Pasteli by downloading the `pasteli` folder from the source code, and importing the folder in your code as if it was a file.

Pasteli depends on the following:
- `xclip` on X11 (`pacman -S xclip` or whatever your distro's equivalent is)
- `wl-clipboard` on Wayland (`pacman -S wl-clipboard` or whatever your distro's equivalent is)
- `pywin32` on Windows (`pip install pywin32`)

When it is eventually on PyPI, it will be able to be installed as follows:

```
pip install pasteli
```

## Examples

```python
>>> import pasteli
>>> pasteli.copy(pasteli.CMODE_TEXT,"hello world, this is pasteli!")
>>> pasteli.paste(pasteli.CMODE_TEXT)
'hello world, this is pasteli!'
>>> pasteli.paste(pasteli.CMODE_TEXT,encoding="bytes")
b'hello world, this is pasteli!'
>>> pasteli.copy(pasteli.CMODE_TEXT,"goodbye world, this was pasteli!")
>>> pasteli.paste(pasteli.CMODE_TEXT)
'goodbye world, this was pasteli!'
```