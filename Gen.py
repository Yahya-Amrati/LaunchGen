from typing import List
import os
import Data_structure
import Utils_net
import shutil
necessities: List[str] = ["launcher.json", "launcher.py", "Utils_minecraft.py", "Utils_net.py", "Data_structure.py"]
def copy_necaissary_files(data: dict) -> None:
    try:
        if data["path"] == "DEFAULT":
            data["path"] = Data_structure.MC_PATH
        Launcher_path: str = os.path.join(data["path"], data["name"]).strip()
        os.makedirs(data["path"], exist_ok=True)
        os.makedirs(Launcher_path, exist_ok=True)
        for i in necessities:
            shutil.copyfile(i, os.path.join(Launcher_path, i))
    except OSError:
        Utils_net.Error_log.error("path is not a valid path")
    except Exception as e:
        Utils_net.Error_log.error("couldn't finish task due to %s",e)
    
def generate_final_product(data: dict) -> None:
    try:
        copy_necaissary_files(data)
        Utils_net.Info_log.info("Copying the necaissary files")
    except OSError:
        Utils_net.Error_log.error("path is not a valid path")
    except Exception as e:
        Utils_net.Error_log.error("couldn't finish task due to %s",e)
