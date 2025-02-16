
import subprocess
from typing import List
import os
import Data_structure
import Utils_minecraft
import Utils_net
import shutil
import sys

necessities: List[str] = ["launcher.json", "dns.json"]


def make_launcher(data: dict) -> None:
    try:
        if data["path"] == "DEFAULT":
            data["path"] = Data_structure.MC_PATH
        elif data["path"] == "LOCAL":
            data["path"] = Utils_minecraft.local_path()

        launcher_path: str = str(os.path.join(data["path"], data["name"]))
        os.makedirs(data["path"], exist_ok=True)
        os.makedirs(launcher_path, exist_ok=True)

        for file in necessities:
            if os.path.exists(file):
                shutil.copyfile(file, os.path.join(launcher_path, file))
            else:
                Utils_net.Error_log.error("Missing required file: %s", file)
                return

        compile_script("Launcher.py", launcher_path)

    except OSError:
        Utils_net.Error_log.error("Path is not a valid path.")
    except Exception as e:
        Utils_net.Error_log.error("Couldn't finish task due to: %s", e)


def compile_script(script_name: str, out: str) -> None:
    try:
        command: List[str] = f"{os.path.join(sys.prefix, 'Scripts', 'pyinstaller') if os.name == 'nt' else os.path.join(sys.prefix, 'bin', 'pyinstaller')} --onefile --distpath {out} {script_name}".split(" ")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        Utils_net.Error_log.error("PyInstaller failed with error: %s", e)
    except Exception as e:
        Utils_net.Error_log.error("Couldn't finish task due to: %s", e)

def generate_final_product(data: dict) -> None:
    try:
        make_launcher(data)
        Utils_net.Info_log.info("Copying the necessary files")
    except Exception as e:
        Utils_net.Error_log.error("Couldn't finish task due to: %s", e)
