import json
import customtkinter as ctk
from tkinter import messagebox
from multiprocessing import freeze_support
import Data_structure
import Utils_minecraft
import Utils_net as un


ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


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
    except Exception as e:
        un.Error_log.error("Couldn't finish task due to %s", e)
        return {}

class LauncherUI:
    def __init__(self, master) -> None:
        self.data = fetch_json()
        self.master = master

        # If JSON data is not loaded, notify the user and exit.
        if not self.data:
            messagebox.showerror(
                "Error",
                "Failed to load launcher.json. Please check the file and try again.",
            )
            master.destroy()
            return

        # Set window title using configuration
        name: str = self.data.get("name", "Minecraft")
        name = name.removeprefix("_") or "Minecraft"
        master.title(f"{name} Launcher")

        # Use default Minecraft path if needed.
        if self.data.get("path", "") == "DEFAULT":
            self.data["path"] = Data_structure.MC_PATH

        # Configure grid weights for the master window.
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        # Create a main frame for all widgets.
        self.main_frame = ctk.CTkFrame(master, corner_radius=10, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Title Label.
        self.title_label = ctk.CTkLabel(
            self.main_frame, text=f"{name} Launcher", font=("Arial", 20, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 20))

        # Username label and entry.
        self.username_label = ctk.CTkLabel(self.main_frame, text="Username:")
        self.username_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.username_entry = ctk.CTkEntry(
            self.main_frame, width=200, placeholder_text="Enter your username"
        )
        self.username_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Launcher version label.
        launcher_version = self.data.get("version_Launcher", "N/A")
        self.version_label = ctk.CTkLabel(
            self.main_frame, text=f"Launcher Version: {launcher_version}"
        )
        self.version_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # Create a frame to display mod options as checkboxes.
        self.mods_frame = ctk.CTkFrame(self.main_frame, corner_radius=5)
        self.mods_frame.grid(
            row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew"
        )
        self.mods_frame.columnconfigure((0, 1, 2), weight=1)

        # Retrieve mod options from configuration.
        is_vanilla = self.data.get("is_vanilla", False)
        is_fabric = self.data.get("is_fabric", False)
        is_forge = self.data.get("is_forge", False)

        # Display mod options as disabled checkboxes.
        self.vanilla_checkbox = ctk.CTkCheckBox(
            self.mods_frame,
            text="Vanilla",
            variable=ctk.BooleanVar(value=is_vanilla),
            state="disabled",
        )
        self.vanilla_checkbox.grid(row=0, column=0, padx=5, pady=5)

        self.fabric_checkbox = ctk.CTkCheckBox(
            self.mods_frame,
            text="Fabric",
            variable=ctk.BooleanVar(value=is_fabric),
            state="disabled",
        )
        self.fabric_checkbox.grid(row=0, column=1, padx=5, pady=5)

        self.forge_checkbox = ctk.CTkCheckBox(
            self.mods_frame,
            text="Forge",
            variable=ctk.BooleanVar(value=is_forge),
            state="disabled",
        )
        self.forge_checkbox.grid(row=0, column=2, padx=5, pady=5)

        # Launch button.
        self.launch_button = ctk.CTkButton(
            self.main_frame,
            text="Launch Minecraft",
            command=self.launch_minecraft,  # Fixed: directly assign the method.
        )
        self.launch_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

        # Status label for feedback.
        self.status_label = ctk.CTkLabel(
            self.main_frame, text="", fg_color="transparent", text_color="gray"
        )
        self.status_label.grid(row=5, column=0, columnspan=2, padx=10, pady=(0, 10))

    def validate_username(self, username: str) -> bool:
        """Validates the username. Returns True if valid, False otherwise."""
        if not username:
            messagebox.showwarning("Input Required", "Please enter a username.")
            return False

        # Assuming Data_structure.LEGAL_CHARS is a set/list of characters that are not allowed.
        for char in username:
            if char not in Data_structure.LEGAL_CHARS:
                messagebox.showwarning(
                    "Invalid Username", "Username contains invalid characters."
                )
                return False

        return True

    def launch_minecraft(self):
        # Clear any previous status message.
        self.status_label.configure(text="")

        # Retrieve and validate the username.
        username = self.username_entry.get().strip()
        if not self.validate_username(username):
            return

        # Update status label to indicate that the launch is in progress.
        self.status_label.configure(text="Launching Minecraft...", text_color="green")
        self.master.update_idletasks()

        try:
            # Call the Minecraft launcher function.
            Utils_minecraft.run_mc(
                self.data.get("version_Launcher"),
                username,
                self.data.get("name"),
                self.data.get("path"),
                [
                    self.data.get("is_vanilla"),
                    False,  # Fabric is not supported yet
                    self.data.get("is_forge")
                ],
            )
            self.status_label.configure(
                text="Minecraft launched successfully!", text_color="green"
            )
        except Exception as e:
            un.Error_log.error("Couldn't finish task due to %s", e)
            messagebox.showerror("Error", f"Failed to launch Minecraft: {e}")
            self.status_label.configure(text="Launch failed.", text_color="red")


def main():
    root = ctk.CTk()
    root.geometry("400x350")  # Set a reasonable window size.
    app = LauncherUI(root)
    root.mainloop()

if __name__ == "__main__":
    freeze_support()
    main()
    un.Info_log.info("Program finished")
