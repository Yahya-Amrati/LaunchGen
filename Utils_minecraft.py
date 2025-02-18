
import multiprocessing
import os
import subprocess
from typing import Callable, List

import minecraft_launcher_lib
import requests
import urllib3
from requests.adapters import HTTPAdapter

import Data_structure as dts
import Utils_net as un

AUTHLIB_INJECTOR_URL: str = (
    "https://github.com/yushijinhun/authlib-injector/releases/download/v1.2.5/authlib-injector-1.2.5.jar"
)
LAUCHEUR_SKELETON_URL: str = (
    ""
)
session = requests.Session()
Retry: urllib3.Retry = urllib3.Retry(
    total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504]
)
session.mount("https://", HTTPAdapter(max_retries=Retry))
session.mount("http://", HTTPAdapter(max_retries=Retry))


def exception_handler(func) -> Callable:
    """this is a decorator for handling exceptions"""

    def wrapper(*args, **kwargs) -> Callable | None:
        try:
            if not un.check_for_internet():
                return un.Error_log.error("No internet connection")
            return func(*args, **kwargs)
        except minecraft_launcher_lib.exceptions.UnsupportedVersion:
            un.Error_log.error("The version is not supported")
        except minecraft_launcher_lib.exceptions.VersionNotFound:
            un.Error_log.error("The version is not found")
        except minecraft_launcher_lib.exceptions.PlatformNotSupported:
            un.Error_log.error("This Platform is not supported")
        except subprocess.CalledProcessError:
            un.Error_log.error("Error in Process call")
        except multiprocessing.ProcessError:
            un.Error_log.error("Error in creating a run mc process")
        except Exception as e:
            un.Error_log.error("Couldn't finish task due to %s", e)
    return wrapper

def install_launcher_skeleton(path: str) -> None:
    """this is a function for installing the launcher skeleton"""
    try:
        DATA = session.get(LAUCHEUR_SKELETON_URL)
        DATA.raise_for_status()
        with open(os.path.join(path, "Launcher.exe"), "wb") as f:
            f.write(DATA.content)
    except requests.exceptions.HTTPError:
        un.Error_log.error("We had a http error while downloading launcher.exe")
    except OSError:
        un.Error_log.error("We had a OSError while downloading launcher.exe")
    except Exception as e:
        un.Error_log.error("Couldn't finish task due to %s", e)

def local_path() -> str:
    """this is a function for getting the local path"""
    return os.path.dirname(os.path.realpath(globals()["__file__"])) or os.getcwd()

def options_check(options: List[bool]) -> bool:
    """checks if only one var in option is set to True"""
    return sum(options) == 1

def install_authlib() -> None:
    """this is a function for installing authlib"""
    try:
        if not un.check_for_internet():
            un.Error_log.error("No internet connection found")
            return
        response = session.get(AUTHLIB_INJECTOR_URL)
        response.raise_for_status()
        un.Info_log.info("Installing authlib")
        os.makedirs(os.path.join(dts.MC_PATH, "cache_dir"), exist_ok=True)
        with open(os.path.join(dts.MC_PATH, "cache_dir", "auth.jar"), "wb") as f:
            f.write(response.content)
    except requests.exceptions.HTTPError:
        un.Error_log.error("We had a http error while downloading auth.jar")
    except OSError:
        un.Error_log.error("We had a OSError while downloading auth.jar")
    except Exception as e:
        un.Error_log.error("Couldn't finish task due to %s", e)

@exception_handler
def install_mc(version: str, option: int) -> None:
    """this is a function for installing a minecraft versions"""
    match option:
        case 1:
            _process: Callable = minecraft_launcher_lib.install.install_minecraft_version
            proc = multiprocessing.Process(target=_process, args=(version, dts.MC_PATH))
            un.Info_log.info("Installing %s", version)
            proc.start()
            proc.join()
        case 2:
            _process: Callable = minecraft_launcher_lib.fabric.install_fabric
            proc = multiprocessing.Process(target=_process, args=(version, dts.MC_PATH))
            un.Info_log.info("Installing %s", version)
            proc.start()
            proc.join()
        case 3:
            version: str = minecraft_launcher_lib.forge.find_forge_version(version)
            _process: Callable = minecraft_launcher_lib.forge.install_forge_version
            proc = multiprocessing.Process(target=_process, args=(version, dts.MC_PATH))
            un.Info_log.info("Installing Forge %s", version)
            proc.start()
            proc.join()
        case _:
            return un.Error_log.error("Invalid option")

def option_check(options: List[bool]) -> int:
    for ix, i in enumerate(options):
        if i:
            options = ix+1
            break
        if ix+1 == len(options):
            options = 1
    return options

def check_is_version_installed(version: str, options: List[bool]) -> None:
    """this is a function for checking if a version is installed"""
    # options = [is_vanilla, is_fabric, is_forge]
    version_ = version

    if options[2]:
        version = running_forge_version(version)
        print("running forge version", version)

    is_exist = any(
        i["id"] == version
        for i in minecraft_launcher_lib.utils.get_installed_versions(dts.MC_PATH)
    )
    if not is_exist:
        install_mc(version_, option_check(options))

def check_is_version_valid(version: str) -> bool:
    """this is a function for checking if a minecraft version is valid"""
    return minecraft_launcher_lib.utils.is_version_valid(version, dts.MC_PATH)

def running_forge_version(version: str) -> str:
    """this is a function for turning vanilla version to forge version"""
    version = minecraft_launcher_lib.forge.find_forge_version(version)
    version = version.split("-")
    return f"{version[0]}-forge-{version[1]}"


@exception_handler
def run_mc(
    version: str, username: str, name: str, path: str, options: List[bool]
) -> None:
    """this is a function for running a minecraft version"""
    if path == "DEFAULT":
        path = dts.MC_PATH
    elif path == "LOCAL":
        path = local_path()
    # waiting till i finish this
    check_is_version_installed(version, options)
    if options[2]:
        version = running_forge_version(version)
    _command: List[str] = minecraft_launcher_lib.command.get_minecraft_command(
        version, path, options=dts.options(username, name, path)
    )
    un.Info_log.info("running minecraft... with %s", _command)
    main_process = subprocess.Popen(args=_command)
    main_process.wait()
    