import os
import subprocess
import minecraft_launcher_lib
import requests
from requests.adapters import HTTPAdapter
import urllib3
import Utils_net as un
import Data_structure as dts
from typing import Callable, List
import multiprocessing
AUTHLIB_URL = "https://github.com/yushijinhun/authlib-injector/releases/download/v1.2.5/authlib-injector-1.2.5.jar"
session = requests.Session()
Retry = urllib3.Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=Retry))
session.mount("http://", HTTPAdapter(max_retries=Retry))

def exception_handler(func) -> Callable:
    """this is a decorator for handling exceptions"""
    def wrapper(*args, **kwargs) -> None | Exception:
        try:        
            if not un.check_for_internet():
                un.Error_log.error("No internet connection")
                return
            func(*args, **kwargs)
        except minecraft_launcher_lib.exceptions.UnsupportedVersion:
            un.Error_log.error("the version is not supported")
        except minecraft_launcher_lib.exceptions.VersionNotFound:
            un.Error_log.error("the version is not found")
        except minecraft_launcher_lib.exceptions.PlatformNotSupported:
            un.Error_log.error("this Platfrom is not supported")
    return wrapper

def options_check(options: List[bool]) -> bool:
    """checks if only one var in option is set to True"""
    return sum(i for i in options if i) > 1

def install_authlib() -> None:
    """this is a function for installing authlib"""
    try:
        if not un.check_for_internet():
            un.Error_log("No internet connection found")
            raise ConnectionError("no internet")
        un.Info_log.info("Installing authlib")
        os.makedirs(os.path.join(dts.MC_PATH, "cache_dir"), exist_ok=True)
        with open(os.path.join(dts.MC_PATH, "cache_dir", "auth.jar"), "wb") as f:
            f.write(session.get(AUTHLIB_URL).content)
    except OSError:
        un.Error_log.error("we had a oserror while downloading auth.jar")
    except Exception as e:
        un.Error_log.error("couldn't finish task due to %s",e)

@exception_handler
def install_mc(version: str, options: List[bool]) -> None:
    """this is a function for installing a minecraft versions"""
    if not options:
        options: List[bool] = [True, False, False]
    elif options_check(options):
        raise ValueError("Only one option can be set to True")
    if options[0]:
        process_: Callable = minecraft_launcher_lib.install.install_minecraft_version
    if options[1]:
        process_: Callable = minecraft_launcher_lib.fabric.install_fabric
    if options[2]:
        version: str = minecraft_launcher_lib.forge.find_forge_version(version)
        process_: Callable = minecraft_launcher_lib.forge.install_forge_version
    un.Info_log.info("Installing %s", version)
    multiprocessing.Process(target=process_, args=(version, dts.MC_PATH)).start()

def run_mc(version: str, username: str) -> None:
    try:
        command: List[str] = minecraft_launcher_lib.command.get_minecraft_command(version, dts.MC_PATH, dts.options(username))
        un.Info_log.info("running minecraft...")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        un.Error_log.error("error in Process call")
    
