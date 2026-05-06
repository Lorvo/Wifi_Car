from cx_Freeze import setup, Executable

setup(name = "auto", version = "1.0", description = "connect to auto", executables = [Executable("main.py", base = "Win32GUI")])