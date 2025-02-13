import customtkinter as ctk
from elements import TopBar, OptionsComboBox
from pathlib import Path
import json
from tkinter import font
from typing import Any

#  █████╗ ██████╗ ██████╗     ██████╗  █████╗  ██████╗ ███████╗███████╗
# ██╔══██╗██╔══██╗██╔══██╗    ██╔══██╗██╔══██╗██╔════╝ ██╔════╝██╔════╝
# ███████║██████╔╝██████╔╝    ██████╔╝███████║██║  ███╗█████╗  ███████╗
# ██╔══██║██╔═══╝ ██╔═══╝     ██╔═══╝ ██╔══██║██║   ██║██╔══╝  ╚════██║
# ██║  ██║██║     ██║         ██║     ██║  ██║╚██████╔╝███████╗███████║
# ╚═╝  ╚═╝╚═╝     ╚═╝         ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝

class Settings(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        
        #self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.controller = controller
        
        buttons = [["Back", lambda: controller.show_frame(WrittingPage)],
                   ["Save Changes", self.save_changes],
                   ]
        self.topBar = TopBar(self, controller, buttons)
        self.topBar.grid(row=0, column=0, sticky="ew")
        
        self.font_size = OptionsComboBox(self, "Font size:", ["16", "24", "32", "48", "64", "80", "96"])
        self.font_size.grid(row=1, column=0, sticky="w", padx=20, pady=20)
        
        self.text_wrapping = OptionsComboBox(self, "Wrap:", ["char", "word", "none"])
        self.text_wrapping.grid(row=2, column=0, sticky="w", padx=20, pady=20)
        
        self.font_family = OptionsComboBox(self, "Font Family:", [str(family) for family in font.families()])
        self.font_family.grid(row=3, column=0, sticky="w", padx=20, pady=20)
        
        self.appearance_mode = OptionsComboBox(self, "Appearance Mode", ["light", "dark"])
        self.appearance_mode.grid(row=4, column=0, sticky="w", padx=20, pady=20)
        
        self.bind("<Expose>", self.update_changes)
        
    def update_changes(self, event: Any = None):
        self.font_size.set_default_value(self.controller.app_settings["font_size"])
        self.text_wrapping.set_default_value(self.controller.app_settings["text_wrapping"])
        self.font_family.set_default_value(self.controller.app_settings["font_family"])
        self.appearance_mode.set_default_value(self.controller.app_settings["appearance_mode"])

    def save_changes(self):
        self.controller.app_settings["font_size"] = int(self.font_size.current_selection())
        self.controller.app_settings["text_wrapping"] = self.text_wrapping.current_selection()
        self.controller.app_settings["font_family"] = self.font_family.current_selection()
        self.controller.app_settings["appearance_mode"] = self.appearance_mode.current_selection()
        
        ctk.set_appearance_mode(self.appearance_mode.current_selection())
        
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
        self.current_file = None
        
        buttons = [["New File", self.new_file],
                   ["Save File", self.save_file],
                   ["Open File", self.load_file],
                   ["Settings", lambda: controller.show_frame(Settings)]
                   ]
        self.topBar = TopBar(self, controller, buttons)
        self.topBar.grid(row=0, column=0, sticky="new")
        
        self.textBox_font = ctk.CTkFont(controller.app_settings["font_family"], controller.app_settings["font_size"])
        self.textBox = ctk.CTkTextbox(self, font=self.textBox_font, wrap=self.controller.app_settings["text_wrapping"])
        self.textBox.grid(row=1, column=0, sticky="nsew")
        
        self.textBox.bind("<Expose>", self.refresh)
        self.textBox.bind("<Control-s>", self.save_file)
    
    def refresh(self, event):
        self.textBox_font.configure(family=self.controller.app_settings["font_family"],
                                    size=self.controller.app_settings["font_size"],)
        self.textBox.focus_set()
        self.textBox.configure(font=self.textBox_font,
                               wrap=self.controller.app_settings["text_wrapping"])
        
    def save_file(self, event: Any = None):      
        filename: str = ctk.filedialog.asksaveasfilename(initialdir=self.user_files_directory,
                                                         initialfile=self.current_file if self.current_file else "",
                                                         title='Save file',
                                                         filetypes=[('Text file', '*.txt')])
        has_filename: bool = True if filename != "" else False
        if has_filename:
            with open(f'{filename}.txt', 'w', encoding='utf-8') as f:
                text: str = str(self.textBox.get('0.0', 'end')).strip()
                f.write(text)
            self.current_file = Path(filename).stem
            self.controller.wm_title(f"MambaWritter - {self.current_file}")

    def load_file(self):
        filename = ctk.filedialog.askopenfilename(initialdir=self.user_files_directory,
                                                  title='Load file',
                                                  filetypes=[('Text file', '*.txt')])
        has_filename: bool = True if filename != "" else False
        if has_filename:
            self.textBox.delete("0.0", "end")
            self.current_file = Path(filename).stem
            self.controller.wm_title(f"MambaWritter - {self.current_file}")
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    self.textBox.insert("0.0", line)

    def new_file(self):
        self.textBox.delete("0.0", "end")
        self.current_file = None
        self.controller.wm_title("MambaWritter")