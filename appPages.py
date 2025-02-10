import customtkinter as ctk
from PIL import Image, ImageTk
from elements import UserFiles

#  █████╗ ██████╗ ██████╗     ██████╗  █████╗  ██████╗ ███████╗███████╗
# ██╔══██╗██╔══██╗██╔══██╗    ██╔══██╗██╔══██╗██╔════╝ ██╔════╝██╔════╝
# ███████║██████╔╝██████╔╝    ██████╔╝███████║██║  ███╗█████╗  ███████╗
# ██╔══██║██╔═══╝ ██╔═══╝     ██╔═══╝ ██╔══██║██║   ██║██╔══╝  ╚════██║
# ██║  ██║██║     ██║         ██║     ██║  ██║╚██████╔╝███████╗███████║
# ╚═╝  ╚═╝╚═╝     ╚═╝         ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝

class Menu(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        
        self.controller = controller
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        logo = ctk.CTkImage(Image.open("assets/AppLogo.png"), size=(720, 180))
        
        self.title = ctk.CTkLabel(self, text="", image=logo)
        self.title.grid(row=0, column=0, sticky="ew")
        
        self.userFiles = UserFiles(self, controller)
        self.userFiles.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
    
    def open_file(self, filepath: str):
        with open(filepath, "r") as f:
            file_content: str = f.read()
        self.controller.show_frame(WrittingPage)
        self.controller.frames[WrittingPage].textBox.insert("1.0", file_content)

class WrittingPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.textBox = ctk.CTkTextbox(self, font=ctk.CTkFont("arial", 16), wrap="word")
        self.textBox.grid(row=0, column=0, sticky="nsew")