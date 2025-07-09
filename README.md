# Pasteli

Pasteli is a cross-platform python library that allows developers to easily access the clipboard, including allowing copying non-text items.

Pasteli is in active development, and may not have complete support for all features on all platforms.

## Support

|Legend|
|------|
|✅ = Working|
|❌ = Not Working|
|➖ = Not Planned|

|Operating System|Windowing System|Support|
|----------------|----------------|---------|
|Windows         |N/A             |❌ (incomplete)|
|MacOS           |N/A             |❌ (incomplete)|
|Linux           |X11             |✅|
|Linux           |Wayland         |❌ (incomplete)|
|iOS             |N/A             |➖|
|iPadOS          |N/A             |➖|
|Android         |N/A             |➖|

> [!WARNING]
> Pasteli may also have problems running on Jython, because `platform.system()` returns `"Java"` on the Jython interpreter, which is used to determine Windows and MacOS operations.