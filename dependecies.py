import subprocess
import sys
from typing import List

# this for dependencies check

libs: List[str] = [
        "minecraft_launcher_lib",
        "customtkinter",
        "streamlit",
        "requests",
        "pyinstaller",
        "urllib3"
        ]

def install():
    """install dependencies"""
    command = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    subprocess.run(command, check=True, text=True)

def check():
    """check if dependencies are installed"""
    for lib in libs:
        try:
            __import__(lib)
        except ImportError:
            install()