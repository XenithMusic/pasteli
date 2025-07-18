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

from . import require as _require

from .core import *
from .constants import *
from . import errors,utils

print(f"PasteLi {VERSION} (on {PY_IMPLEMENTATION} {PY_VERSION})")