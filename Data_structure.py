import sys
import subprocess
import os
import uuid
from typing import List
from dataclasses import dataclass, field
import Utils_minecraft as mcutils

try:
    import minecraft_launcher_lib
except ImportError:
    try:
        command = [
            sys.executable,
            "-m",
            "pip",
            "install",
            "minecraft_launcher_lib",
        ]  # pip install minecraft_launcher_lib
        subprocess.run(command, check=True, text=True)
    except subprocess.CalledProcessError as e:
        raise ImportError from e

# cette Partie à été coder entierment par Yahya Amrati
# 05/02/2025

LEGAL_CHARS: set = set(
    """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"""
)


def get_appdata_universal() -> str:
    """returns the universal appdata path"""
    if sys.platform == "win32":
        return os.getenv("APPDATA")
    elif sys.platform.startswith("linux"):
        return os.getenv("XDG_CONFIG_HOME")
    elif sys.platform == "darwin":
        return os.getenv("HOME")
    else:
        raise OSError("Unsupported platform")


MC_PATH = os.path.join(get_appdata_universal(), "Minecraft")
os.makedirs(MC_PATH, exist_ok=True)


def generate_random_username() -> str:
    """
    this function will generate a random username
     conforming to the rules of minecraft usernames
    """
    uuid__name: str = str(uuid.uuid4())
    name: list = []
    for ix, i in enumerate(uuid__name.split("-")):
        # checking if for not letting the username be too long
        # cause max username in minecraft length is 16
        if ix == 15:
            break
        for x in i.split():
            if x not in LEGAL_CHARS:
                i = i.replace(x, "")
            else:
                continue
        name.append(i)
    return "".join(name)


@dataclass
class UserMinecraft:
    """
    this a data class containing all the data of a minecraft user instance
    """

    uuid: str
    name: str = generate_random_username()
    offline: bool = True
    vanilla: bool = True
    forge: bool = False
    fabric: bool = False

    def __init__(self):
        # correct values if possible
        new_name: list = []
        for i in self.name:
            if i not in LEGAL_CHARS:
                i = ""
            new_name.append(i)
        self.name = "".join(new_name)
        if self.vanilla:
            self.forge = False
            self.fabric = False
        elif self.forge:
            self.vanilla = False
            self.fabric = False
        elif self.fabric:
            self.vanilla = False
            self.forge = False
        self.uuid = str(uuid.uuid3(uuid.RESERVED_MICROSOFT, self.name))


@dataclass
class MinecraftInstances:
    """
    this a data class containing all the data of a minecraft instance
    """

    names: List[str] = field(default_factory=list)

    def __init__(self) -> None:
        self.names = [
            i["id"]
            for i in minecraft_launcher_lib.utils.get_installed_versions(MC_PATH)
        ]

@dataclass
class MinecraftLauncher:
    name: str
    path: str = "DEFAULT"
    is_forge: bool = False
    is_fabric: bool = False
    is_vanilla: bool = True
    crack_supported: bool = True
    version_Launcher: str = "1.16.5"

def options(username: str) -> List[str]:
    mcutils.install_authlib()
    options: List[str] = {
        # This is needed
        "username": username,
        "uuid": str(uuid.uuid3(namespace=uuid.NAMESPACE_URL, name=username)),
        "token": "",
        # This is optional
        "executablePath": "java", # The path to the java executable
        "defaultExecutablePath": "java", # The path to the java executable if the client.json has none
        "jvmArguments": [f"-javaagent:{os.path.join(MC_PATH, "cache_dir", "auth.jar")}=ely.by"], #The jvmArguments
        "launcherName": "MyLauncher", # The name of your launcher
        "launcherVersion": "1.0", # The version of your launcher
        "demo": False, # Run Minecraft in demo mode
        "customResolution": False, # Enable custom resolution
        "resolutionWidth": "854", # The resolution width
        "resolutionHeight": "480", # The resolution height
        "enableLoggingConfig": False, # Enable use of the log4j configuration file
        "disableMultiplayer": False, # Disables the multiplayer
    }
    return options