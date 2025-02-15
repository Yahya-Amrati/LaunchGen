import subprocess
import sys
# this for dependecies check
libs = ["minecraft_launcher_lib",
        "customtkinter",
        "streamlit",
        "requests",
        "pyinstaller",
        "urllib3"
        ]

def install():
    """install dependecies"""
    command = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    subprocess.run(command, check=True, text=True)

def check():
    """check if dependecies are installed"""
    for lib in libs:
        try:
            __import__(lib)
        except ImportError:
            install()