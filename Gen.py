import subprocess
from typing import List
import os
import Data_structure
import Utils_minecraft
import Utils_net
import shutil
import sys
necessities: List[str] = ["launcher.json", "dns.json", "launcher.json"]
def make_launcher(data: dict) -> None:
    try:
        if data["path"] == "DEFAULT":
            data["path"] = Data_structure.MC_PATH
        if data["path"] == "LOCAL":
            data["path"] = Utils_minecraft.LocalPath()
        Launcher_path: str = os.path.join(data["path"], data["name"]).strip()
        os.makedirs(data["path"], exist_ok=True)
        os.makedirs(Launcher_path, exist_ok=True)
        for i in necessities:
            shutil.copyfile(i, os.path.join(Launcher_path, i))
        compile("Launcher.py", Launcher_path)
    except OSError:
        Utils_net.Error_log.error("path is not a valid path")
    except Exception as e:
        Utils_net.Error_log.error("couldn't finish task due to %s",e)

def compile(script_name: str, out: str) -> None:
    
    try:
        COMMAND: str = f"{sys.executable} -m pyinstaller --onefile --distpath {out} {script_name}"
        COMMAND: List[str] = COMMAND.split(" ")
        subprocess.run(COMMAND)
    except Exception as e:
        Utils_net.Error_log.error("couldn't finish task due to %s",e)
        
def generate_final_product(data: dict) -> None:
    try:
        make_launcher(data)
        Utils_net.Info_log.info("Copying the necaissary files")
    except OSError:
        Utils_net.Error_log.error("path is not a valid path")
    except Exception as e:
        Utils_net.Error_log.error("couldn't finish task due to %s",e)
