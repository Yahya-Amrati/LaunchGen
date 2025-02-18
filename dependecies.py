import subprocess
import sys
import downloads
import os
from typing import List
import Utils_net

# this for dependencies check

libs: List[str] = [
        "minecraft_launcher_lib",
        "customtkinter",
        "streamlit",
        "requests",
        "pyinstaller",
        "urllib3"
        ]

def install(path: str) -> None:
    """install dependencies"""
    print("Installing dependencies...")
    print(f"Path: {path}")
    command = [sys.executable, "-m", "pip", "install", "-r", f"{os.path.join(path, 'requirements.txt')}"]
    subprocess.run(command, check=True, text=True)

def check(path: str) -> None:
    """check if dependencies are installed"""
    try:
        for lib in libs:
            __import__(lib)
    except ImportError:
        if not Utils_net.check_for_internet():
            Utils_net.Info_log.info("No internet connection found")
            return
        install(path)