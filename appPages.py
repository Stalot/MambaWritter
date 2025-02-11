import customtkinter as ctk
from PIL import Image, ImageTk
from elements import TopBar, Value
from pathlib import Path
import json

#  █████╗ ██████╗ ██████╗     ██████╗  █████╗  ██████╗ ███████╗███████╗
# ██╔══██╗██╔══██╗██╔══██╗    ██╔══██╗██╔══██╗██╔════╝ ██╔════╝██╔════╝
# ███████║██████╔╝██████╔╝    ██████╔╝███████║██║  ███╗█████╗  ███████╗
# ██╔══██║██╔═══╝ ██╔═══╝     ██╔═══╝ ██╔══██║██║   ██║██╔══╝  ╚════██║
# ██║  ██║██║     ██║         ██║     ██║  ██║╚██████╔╝███████╗███████║
# ╚═╝  ╚═╝╚═╝     ╚═╝         ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝

class Settings(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        
        self.controller = controller
        
        buttons = [["Back", lambda: controller.show_frame(WrittingPage)],
                   ["Save Changes", self.save_changes],
                   ]
        self.topBar = TopBar(self, controller, buttons)
        self.topBar.grid(row=0, column=0, sticky="new")
        
        self.font_size = Value(self, controller)
        self.font_size.grid(row=1, column=0)
    
    def save_changes(self):
        data ={"font_size": int(self.font_size.display.get()),
               "font_family": "Arial"}
        with open("cache/custom_app_settings.json", "w") as f:
            f.write(json.dumps(data))
            self.controller.app_settings = data

class WrittingPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.controller = controller
        
        self.user_files_directory = Path.home().joinpath("Documents/MambaWritter").as_posix()
        
        buttons = [["Save File", self.save_file],
                   ["Open File", self.load_file],
                   ["Settings", lambda: controller.show_frame(Settings)]
                   ]
        self.topBar = TopBar(self, controller, buttons)
        self.topBar.grid(row=0, column=0, sticky="new")
        
        self.textBox_font = ctk.CTkFont(controller.app_settings["font_family"], controller.app_settings["font_size"])
        self.textBox = ctk.CTkTextbox(self, font=self.textBox_font, wrap="word")
        self.textBox.grid(row=1, column=0, sticky="nsew")
        
        self.textBox.bind("<Expose>", self.refresh)
    
    def refresh(self, event):
        self.textBox_font.configure(family=self.controller.app_settings["font_family"],
                                    size=self.controller.app_settings["font_size"])
        self.textBox.configure(font=self.textBox_font)
    
    def save_file(self):      
        filename: str = ctk.filedialog.asksaveasfilename(initialdir=self.user_files_directory,
                                                         title='Save file',
                                                         filetypes=[('Text file', '*.txt')])
        has_filename: bool = True if filename != "" else False
        if has_filename:
            with open(f'{filename.strip()}.txt', 'w', encoding='utf-8') as f:
                text: str = str(self.textBox.get('0.0', 'end')).strip()
                f.write(text)

    def load_file(self):
        filename = ctk.filedialog.askopenfilename(initialdir=self.user_files_directory,
                                                  title='Load file',
                                                  filetypes=[('Text file', '*.txt')])
        with open(filename, 'r', encoding='utf-8') as f:
            text: str = str(f.read()).strip()
        
        self.textBox.delete("0.0", "end")
        self.textBox.insert("0.0", text)