import minecraft_launcher_lib
import Utils_net as un
import Data_structure as dts
from typing import Callable, List

def exception_handler(func) -> Callable:
    def wrapper(*args, **kwargs) -> None:
        try:        
            if not un.is_internet_connected():
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
    true_counter = sum(i for i in options if i)
    return true_counter > 1

@exception_handler
def install_mc(version: str, options: List[bool], path: str = dts.MC_PATH) -> None:
    if not options:
        options = [True, False, False]
    elif options_check(options):
        raise ValueError("Only one option can be set to True")
    if options[0]:
        minecraft_launcher_lib.install.install_minecraft_version(version, path)
    if options[1]:
        minecraft_launcher_lib.fabric.install_fabric(version, path)
    if options[2]:
        version = minecraft_launcher_lib.forge.find_forge_version(version)
        minecraft_launcher_lib.forge.install_forge_version(version, path)
