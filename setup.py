import sys
from cx_Freeze import setup, Executable

setup(
    name = "pydice",
    version = "0.1",
    description = "lp",
    executables = [Executable("freezingdice.py", base="Win32GUI")] )