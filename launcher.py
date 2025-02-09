import json
import minecraft_launcher_lib
import Utils_minecraft
if __name__ == "__main__":
    # to be continued
    with open("launcher.json", "r") as f:
        data = json.load(f)
        Utils_minecraft.run_mc(data["version_Launcher"], data["options"])
        