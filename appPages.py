import customtkinter as ctk
from PIL import Image, ImageTk
from elements import TopBar, OptionsComboBox
from pathlib import Path
import json
from fileManagement import path

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
        
        self.font_size = OptionsComboBox(self, "Font size:", ["4", "8", "16", "24", "32", "48", "64", "80", "96"])
        self.font_size.grid(row=1, column=0, sticky="w", padx=20, pady=20)
        self.font_size.set_default_value(self.controller.app_settings["font_size"])
        
        self.text_wrapping = OptionsComboBox(self, "Wrap:", ["char", "word", "none"])
        self.text_wrapping.grid(row=2, column=0, sticky="w", padx=20, pady=20)
        self.text_wrapping.set_default_value(self.controller.app_settings["text_wrapping"])

    def save_changes(self):
        self.controller.app_settings["font_size"] = int(self.font_size.current_selection())
        self.controller.app_settings["text_wrapping"] = self.text_wrapping.current_selection()
        with open(self.controller.custom_settings_json_path, "w") as f:
            new_data: dict = self.controller.app_settings
            f.write(json.dumps(new_data))

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
        self.textBox = ctk.CTkTextbox(self, font=self.textBox_font, wrap=self.controller.app_settings["text_wrapping"])
        self.textBox.grid(row=1, column=0, sticky="nsew")
        
        self.textBox.bind("<Expose>", self.refresh)
    
    def refresh(self, event):
        self.textBox_font.configure(family=self.controller.app_settings["font_family"],
                                    size=self.controller.app_settings["font_size"],)
        self.textBox.focus_set()
        self.textBox.configure(font=self.textBox_font,
                               wrap=self.controller.app_settings["text_wrapping"])
    
    def save_file(self):      
        filename: str = ctk.filedialog.asksaveasfilename(initialdir=self.user_files_directory,
                                                         title='Save file',
                                                         filetypes=[('Text file', '*.txt')])
        has_filename: bool = True if filename != "" else False
        if has_filename:
            with open(f'{filename}.txt', 'w', encoding='utf-8') as f:
                text: str = str(self.textBox.get('0.0', 'end')).strip()
                f.write(text)

    def load_file(self):
        filename = ctk.filedialog.askopenfilename(initialdir=self.user_files_directory,
                                                  title='Load file',
                                                  filetypes=[('Text file', '*.txt')])
        has_filename: bool = True if filename != "" else False
        if has_filename:
            with open(filename, 'r', encoding='utf-8') as f:
                text: str = str(f.read()).strip()
            
            self.textBox.delete("0.0", "end")
            self.textBox.insert("0.0", text)