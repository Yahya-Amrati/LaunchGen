
import sys
import os
import uuid
from typing import List
from dataclasses import dataclass, field
import Utils_minecraft as mcutils
import Utils_net as un
import minecraft_launcher_lib

# 05/02/2025
# 16/02/2025

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

    def __post_init__(self):
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
        self.uuid = str(uuid.uuid3(uuid.NAMESPACE_URL, self.name))


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
    is_fabric: None = None
    is_vanilla: bool = True
    crack_supported: bool = True
    version_Launcher: str = "1.16.5"
    def __post_init__(self) -> None:
        if self.is_forge:
            self.is_vanilla = False
            self.is_fabric = None
        elif self.is_fabric:
            un.Error_log.error("fabric is not supported yet")
        elif self.is_vanilla:
            self.is_forge = False

def options(username: str, name: str, path: str):
    new_name: list = []
    for i in username:
        if i not in LEGAL_CHARS:
            i: str = ""
        new_name.append(i)
    username: str = "".join(new_name)
    mcutils.install_authlib()
    return {
        "username": username,
        "uuid": str(uuid.uuid3(namespace=uuid.NAMESPACE_URL, name=username)),
        "token": "",
        "gameDirectory": path,
        "executablePath": f"{minecraft_launcher_lib.utils.get_java_executable()}",
        "defaultExecutablePath": "java",
        "jvmArguments": [
            f"-javaagent:{os.path.join(MC_PATH, "cache_dir", "auth.jar")}=ely.by"
        ],
        "launcherName": name,
        "launcherVersion": "1.0",
        "demo": False,
        "customResolution": False,
        "resolutionWidth": "854",
        "resolutionHeight": "480",
        "enableLoggingConfig": False,
        "disableMultiplayer": False,
    }

