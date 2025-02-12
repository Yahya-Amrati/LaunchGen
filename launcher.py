import json
import tkinter as tk
from tkinter import messagebox
from multiprocessing import freeze_support
import Data_structure
import Utils_minecraft
import Utils_net as un

def fetch_json() -> dict:
    try:
        with open("launcher.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError:
        un.Error_log.error("launcher.json is not a valid json file")
        return {}
    except FileNotFoundError:
        un.Error_log.error("launcher.json not found")
        return {}
    except PermissionError:
        un.Error_log.error("launcher.json is not accessible due to lack of permission")
        return {}
    except UnicodeTranslateError:
        un.Error_log.error("launcher.json has not a valid encoding type")
        return {}

class LauncherUI:
    def __init__(self, master):
        self.master = master
        master.title("Minecraft Launcher")

        # Load configuration from JSON.
        self.data = fetch_json()
        if not self.data:
            messagebox.showerror("Error", "Failed to load launcher.json. Please check the file and try again.")
            master.destroy()
            return

        # If the path is set to "DEFAULT", use the default Minecraft path from Data_structure.
        if self.data.get("path", "") == "DEFAULT":
            self.data["path"] = Data_structure.MC_PATH

        # --- Create UI widgets ---

        # Username label and entry.
        self.username_label = tk.Label(master, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.username_entry = tk.Entry(master, width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # Display the launcher version.
        launcher_version = self.data.get("version_Launcher", "N/A")
        self.version_label = tk.Label(master, text=f"Launcher Version: {launcher_version}")
        self.version_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        # Display mod options (vanilla, fabric, forge).
        vanilla = self.data.get("is_vanilla", False)
        fabric = self.data.get("is_fabric", False)
        forge = self.data.get("is_forge", False)
        self.mods_label = tk.Label(master, text=f"Vanilla: {vanilla} | Fabric: {fabric} | Forge: {forge}")
        self.mods_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # Launch button.
        self.launch_button = tk.Button(master, text="Launch Minecraft", command=self.launch_minecraft)
        self.launch_button.grid(row=3, column=0, columnspan=2, padx=10, pady=20)

    def launch_minecraft(self):
        # Retrieve the username entered by the user.
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showwarning("Input Required", "Please enter your username.")
            return

        try:
            # Call the Minecraft launcher function.
            # The run_mc function parameters are:
            #   1. version from the launcher,
            #   2. username,
            #   3. version (again, as per your original call),
            #   4. the path,
            #   5. a list of booleans indicating [is_vanilla, is_fabric, is_forge].
            Utils_minecraft.run_mc(
                self.data.get("version_Launcher"),
                username,
                self.data.get("version_Launcher"),
                self.data.get("path"),
                [self.data.get("is_vanilla"), self.data.get("is_fabric"), self.data.get("is_forge")]
            )
        except Exception as e:
            un.Error_log.error("Couldn't finish task due to %s", e)
            messagebox.showerror("Error", f"Failed to launch Minecraft: {e}")

def main():
    root = tk.Tk()
    app = LauncherUI(root)
    root.mainloop()

if __name__ == '__main__':
    freeze_support()    
    main()
    un.Info_log.info("Program finished")