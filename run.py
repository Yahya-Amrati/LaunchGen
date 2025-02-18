# sourcery skip: use-fstring-for-concatenation
import sys
import os
import subprocess
import dependecies
import downloads

file_dependencies = ["UI.py", "downloads.py", "Utils_minecraft.py", "dependecies.py", "Gen.py", "Data_structure.py", "Utils_net.py"]
def call(path: str) -> None:
    """this is a function for calling other functions"""
    downloads.main()
    dependecies.install(path)
    return
path = downloads.path
for i in file_dependencies:
    if not os.path.exists(os.path.join(path, i)):
        print("Downloading dependencies on path ", path)
        call(path)
        break

def resolve_path(path_):
    """this is a function for resolving the path"""
    return os.path.abspath(os.path.join(path, path_))
os.chdir(path)
command = ["streamlit", "run", "UI.py", "--global.developmentMode=false"]
subprocess.run(command, check=True, text=True)
sys.exit()
