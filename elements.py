import customtkinter as ctk
from pathlib import Path
from PIL import Image
from fileManagement import path

# ███████╗██╗     ███████╗███╗   ███╗███████╗███╗   ██╗████████╗███████╗
# ██╔════╝██║     ██╔════╝████╗ ████║██╔════╝████╗  ██║╚══██╔══╝██╔════╝
# █████╗  ██║     █████╗  ██╔████╔██║█████╗  ██╔██╗ ██║   ██║   ███████╗
# ██╔══╝  ██║     ██╔══╝  ██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║   ╚════██║
# ███████╗███████╗███████╗██║ ╚═╝ ██║███████╗██║ ╚████║   ██║   ███████║
# ╚══════╝╚══════╝╚══════╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝

class Value(ctk.CTkFrame):
    def __init__(self,
                 master,
                 controller):
        super().__init__(master)
        
        self.display = ctk.CTkEntry(self, placeholder_text="32")
        self.increase_button = ctk.CTkButton(self, text="+")
        self.decrease_button = ctk.CTkButton(self, text="-")
        
        self.display.grid(row=0, column=1, sticky="ew")
        self.increase_button.grid(row=0, column=0, sticky="e")
        self.decrease_button.grid(row=0, column=2, sticky="w")

class TopBar(ctk.CTkFrame):
    def __init__(self,
                 master,
                 controller,
                 buttons: list[list]):
        super().__init__(master)
        
        c = 0
        for b in buttons:
            new_button = ctk.CTkButton(self, text=b[0], command=b[1])
            new_button.grid(row=0, column=c, padx=10)
            c += 1