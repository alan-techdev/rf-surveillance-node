"""Module containing bug report helper(s)."""

import json
import platform
import sys
from typing import Any

import numpy  # type:ignore
import pyrtlsdrlib  #type:ignore
import rtlsdr  # type:ignore
import serial  # type:ignore

from . import __version__ as rfnode_version


def _implementation()-> Any:
    """Return a dict with the Python implementation and version.

    Provide both the name and the version of the Python implementation
    currently running. For example, on CPython 3.10.3 it will return
    {'name': 'CPython', 'version': '3.10.3'}.

    This function works best on CPython and PyPy: in particular, it probably
    doesn't work for Jython or IronPython. Future investigation should be done
    to work out the correct shape of the code for those platforms.
    """
    implementation = platform.python_implementation()

    if implementation == "CPython":
        implementation_version = platform.python_version()
    elif implementation == "PyPy":
        pypy = sys.pypy_version_info  # type: ignore[attr-defined]
        implementation_version = f"{pypy.major}.{pypy.minor}.{pypy.micro}"  # pyright: ignore[reportUnknownMemberType]
        if sys.pypy_version_info.releaselevel != "final":  # type: ignore[attr-defined]
            implementation_version = "".join(
                [implementation_version, sys.pypy_version_info.releaselevel]  # type: ignore[attr-defined]
            )
    elif implementation == "Jython":
        implementation_version = platform.python_version()  # Complete Guess
    elif implementation == "IronPython":
        implementation_version = platform.python_version()  # Complete Guess
    else:
        implementation_version = "Unknown"

    return {"name": implementation, "version": implementation_version}


def info() -> dict[str, Any]:
    """Generate information for a bug report."""
    try:
        platform_info = {
            "system": platform.system(),
            "release": platform.release(),
        }
    except OSError:
        platform_info = {
            "system": "Unknown",
            "release": "Unknown",
        }

    implementation_info = _implementation()
    rfnode_info = {"version": rfnode_version}
    rtlsdr_info = {"version:": rtlsdr.__version__}
    pyrtlsdrlib_info = {"min version:" : pyrtlsdrlib.PYRTLSDR_MIN_VERSION}
    serial_info = {"version": serial.__version__}
    numpy_info =  {"version": numpy.__version__}


    return {
        "platform": platform_info,
        "implementation": implementation_info,
        "rtlsdr_info": rtlsdr_info,
        "pyrtlsdrlib_info": pyrtlsdrlib_info,
        "serial_info" :serial_info,
        "numpy_info": numpy_info,
        "rfnode": {
            "version": rfnode_info,
        },
    }


def bug_reporting()-> None:
    """Pretty-print the bug information as JSON."""
    print(json.dumps(info(), sort_keys=True, indent=2))


if __name__ == "__main__":
    bug_reporting()
