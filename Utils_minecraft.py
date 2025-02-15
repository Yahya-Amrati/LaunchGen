import dependecies ; dependecies.check()  # noqa: E702
import os
import subprocess
import sys
import Utils_net as un
import Data_structure as dts
from typing import Callable, List
import multiprocessing
import minecraft_launcher_lib
import requests
from requests.adapters import HTTPAdapter
import urllib3

AUTHLIB_INJECTOR_URL = "https://github.com/yushijinhun/authlib-injector/releases/download/v1.2.5/authlib-injector-1.2.5.jar"
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
            return func(*args, **kwargs)
        except minecraft_launcher_lib.exceptions.UnsupportedVersion:
            un.Error_log.error("the version is not supported")
        except minecraft_launcher_lib.exceptions.VersionNotFound:
            un.Error_log.error("the version is not found")
        except minecraft_launcher_lib.exceptions.PlatformNotSupported:
            un.Error_log.error("this Platfrom is not supported")
        except subprocess.CalledProcessError:
            un.Error_log.error("error in Process call")
        except multiprocessing.ProcessError:
            un.Error_log.error("Error in creating a run mc process")
    return wrapper

def LocalPath() -> str:
    """this is a function for getting the local path"""
    return os.path.dirname(os.path.realpath(globals()["__file__"])) or os.getcwd()

def options_check(options: List[bool]) -> bool:
    """checks if only one var in option is set to True"""
    return sum(options) == 1

def install_authlib() -> None:
    """this is a function for installing authlib"""
    try:
        if not un.check_for_internet():
            un.Error_log("No internet connection found")
            raise ConnectionError("no internet")
        un.Info_log.info("Installing authlib")
        os.makedirs(os.path.join(dts.MC_PATH, "cache_dir"), exist_ok=True)
        with open(os.path.join(dts.MC_PATH, "cache_dir", "auth.jar"), "wb") as f:
            f.write(session.get(AUTHLIB_INJECTOR_URL).content)
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
    elif options[1]:
        process_: Callable = minecraft_launcher_lib.fabric.install_fabric
    elif options[2]:
        version: str = minecraft_launcher_lib.forge.find_forge_version(version)
        process_: Callable = minecraft_launcher_lib.forge.install_forge_version
    else:
        def process_() -> Exception:
            raise ValueError("No option is set to True")

    un.Info_log.info("Installing %s", version)
    proc = multiprocessing.Process(target=process_, args=(version, dts.MC_PATH))
    proc.start()
    proc.join()

def check_is_version_installed(version: str, options: List[bool]) -> bool:
    """this is a function for checking if a version is installed"""
    if options[1]:
        return False
    if options[2]:
        version = minecraft_launcher_lib.forge.find_forge_version(version)
        version = version.split("-")
        version = f"{version[0]}-forge-{version[1]}"
    return any(i["id"] == version for i in minecraft_launcher_lib.utils.get_installed_versions(dts.MC_PATH))

def check_is_version_valid(version: str) -> bool:
    """this is a function for checking if a minecraft version is valid"""
    return minecraft_launcher_lib.utils.is_version_valid(version, dts.MC_PATH)

def running_forge_version(version: str) -> str:
    """this is a function for turning vanilla version to forge version"""
    version = minecraft_launcher_lib.forge.find_forge_version(version)
    version = version.split("-")
    version = f"{version[0]}-forge-{version[1]}"
    return version

@exception_handler
def run_mc(version: str, username: str, name: str, path: str ,options: List[bool]) -> None:
    """this is a function for running a minecraft version"""
    if path == "DEFAULT":
        path = dts.MC_PATH
    elif path == "LOCAL":
        path = LocalPath()
    # waiting till i finish this
    if not check_is_version_installed(version, options):
        un.Error_log.error("the version here is not installed")
        if check_is_version_valid(version):
            install_mc(version, options)
    if options[2]:
        version = running_forge_version(version)
    command: List[str] = minecraft_launcher_lib.command.get_minecraft_command(version, dts.MC_PATH,
                                                                              dts.options(username, name, path))
    un.Info_log.info("running minecraft...")
    sub_proc_inst: Callable = subprocess.Popen
    mainproc = sub_proc_inst(command)
    mainproc.wait()

