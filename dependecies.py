import subprocess
import sys
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

def install():
    """install dependencies"""
    print("Installing dependencies...")
    command = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    subprocess.run(command, check=True, text=True)

def check():
    """check if dependencies are installed"""
    for lib in libs:
        try:
            __import__(lib)
        except ImportError:
            if not Utils_net.check_for_internet():
                Utils_net.Info_log.info("No internet connection found")
                exit(1)
            install()
            break