import tkinter as tk
import ttkbootstrap as ttk
import json
from dataclasses import asdict
from Data_structure import MinecraftLauncher
# Assuming MinecraftLauncher is in this file
# this was made with chatgpt, but the other files are from me except this one
class UI:
    def __init__(self) -> None:
        self.root = ttk.Window("LaunchGen", themename="flatly")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        
        # Initialize variables that will be set during the pages
        self.Launcher_Name = ""
        self.Launcher_Version = ""
        self.Launcher_base = ""
        self.is_vanilla = False
        self.is_fabric = False
        self.is_forge = False
        self.crack_supported = False
        
        # Start with the first page
        self.page1()
        self.root.mainloop()

    def page1(self) -> None:
        ttk.Label(self.root, text="LaunchGen", font=("Helvetica", 30, "bold"), foreground="#4E8CFF").pack(pady=40)
        ttk.Label(self.root, text="Input your launcher name", font=("Helvetica", 18)).pack(pady=15)
        
        entry1 = ttk.Entry(self.root, font=("Helvetica", 14), justify="center")
        entry1.pack(pady=15, ipady=5, ipadx=10)
        
        def switch() -> None:
            self.Launcher_Name = entry1.get().title()
            self.page2()

        ttk.Button(self.root, text="Next", style="success.TButton", command=switch).pack(pady=20)

    def page2(self) -> None:
        # Clear window content before adding new elements
        for widget in self.root.winfo_children():
            widget.destroy()
        
        ttk.Label(self.root, text="LaunchGen", font=("Helvetica", 30, "bold"), foreground="#4E8CFF").pack(pady=40)
        ttk.Label(self.root, text="Choose your launcher base", font=("Helvetica", 18)).pack(pady=15)

        entry1 = tk.Listbox(self.root, font=("Helvetica", 14), selectmode="single", height=4)
        entry1.insert(1, "Vanilla")
        entry1.insert(2, "Fabric")
        entry1.insert(3, "Forge")
        entry1.pack(pady=15, ipadx=10, ipady=5)

        def switch() -> None:
            index = entry1.curselection()
            bases = ["Vanilla", "Fabric", "Forge"]
            if index:
                self.Launcher_base = bases[index[0]]
                self.is_vanilla = (self.Launcher_base == "Vanilla")
                self.is_fabric = (self.Launcher_base == "Fabric")
                self.is_forge = (self.Launcher_base == "Forge")
            self.page3()

        ttk.Button(self.root, text="Next", style="info.TButton", command=switch).pack(pady=20)

    def page3(self) -> None:
        # Clear window content before adding new elements
        for widget in self.root.winfo_children():
            widget.destroy()
        
        ttk.Label(self.root, text="LaunchGen", font=("Helvetica", 30, "bold"), foreground="#4E8CFF").pack(pady=40)
        ttk.Label(self.root, text="Enter your launcher MC version", font=("Helvetica", 18)).pack(pady=15)
        
        entry1 = ttk.Entry(self.root, font=("Helvetica", 14), justify="center")
        entry1.pack(pady=15, ipady=5, ipadx=10)

        def switch() -> None:
            self.Launcher_Version = entry1.get()
            self.finish_page()

        ttk.Button(self.root, text="Next", style="warning.TButton", command=switch).pack(pady=20)

    def finish_page(self) -> None:
        # Clear window content before adding new elements
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create the MinecraftLauncher dataclass instance with all gathered data
        try:
            launcher = MinecraftLauncher(
                name=self.Launcher_Name,
                is_forge=self.is_forge,
                is_fabric=self.is_fabric,
                is_vanilla=self.is_vanilla,
                version_Launcher=self.Launcher_Version
            )
        except TypeError as e:
            print(f"Error while creating MinecraftLauncher: {e}")
            return

        # Convert the dataclass to a dictionary for easy JSON serialization
        launcher_data = asdict(launcher)

        # Write the collected data into a JSON file
        with open("launcher.json", "w") as json_file:
            json.dump(launcher_data, json_file, indent=4)

        # Display the final gathered information
        ttk.Label(self.root, text="LaunchGen", font=("Helvetica", 30, "bold"), foreground="#4E8CFF").pack(pady=40)
        ttk.Label(self.root, text="Your Launcher Information:", font=("Helvetica", 22, "bold")).pack(pady=20)

        ttk.Label(self.root, text=f"Launcher Name: {launcher.name}", font=("Helvetica", 14)).pack(pady=5)
        ttk.Label(self.root, text=f"Base: {'Vanilla' if launcher.is_vanilla else 'Fabric' if launcher.is_fabric else 'Forge'}", font=("Helvetica", 14)).pack(pady=5)
        ttk.Label(self.root, text=f"Version: {launcher.version_Launcher}", font=("Helvetica", 14)).pack(pady=5)
        ttk.Button(self.root, text="Exit", style="danger.TButton", command=self.root.quit).pack(pady=30)

UI()
