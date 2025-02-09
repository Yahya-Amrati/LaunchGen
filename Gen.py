import json
import os
import Data_structure
import Utils_net
import shutil

def fetch_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def copy_necaissary_files(data: dict) -> None:
    if data["path"] == "DEFAULT":
            data["path"] = Data_structure.MC_PATH

    Launcher_path: str = os.path.join(data["path"], data["name"]).strip()
    os.makedirs(data["path"], exist_ok=True)
    os.makedirs(Launcher_path, exist_ok=True)
    shutil.copyfile("launcher.json", os.path.join(Launcher_path, "launcher.json"))
    shutil.copyfile("launcher.py", os.path.join(Launcher_path, "launcher.py"))
    shutil.copyfile("Utils_minecraft.py", os.path.join(Launcher_path, "Utils_minecraft.py"))
    shutil.copyfile("Utils_net.py", os.path.join(Launcher_path, "Utils_net.py"))
    shutil.copyfile("Data_structure.py", os.path.join(Launcher_path, "Data_structure.py"))
    
def generate_final_product(data: dict) -> None:
    try:
        data = fetch_json("launcher.json")
        copy_necaissary_files(data)
        Utils_net.Info_log.info("Copying the necaissary files")
    except OSError:
        Utils_net.Error_log.error("path is not a valid path")
    except Exception as e:
        Utils_net.Error_log.error("couldn't finish task due to %s",e)
