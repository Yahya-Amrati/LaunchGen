import sys
import subprocess


"""pip install -r requirements.txt"""
libs = ["minecraft_launcher_lib", "customtkinter", "streamlit", "requests", "pyinstaller", "urllib3"]
def install():
    command = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    subprocess.run(command, check=True, text=True)

def check():
    for lib in libs:
        try:
            __import__(lib)
        except ImportError:
            install()