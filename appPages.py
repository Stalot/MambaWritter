from elements import TopBar, OptionsComboBox
from tkinter import font
from typing import Any
import customtkinter as ctk
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
        
        self.text_wrapping = OptionsComboBox(self, "Wrap:", ["Char", "Word", "None"])
        self.text_wrapping.grid(row=2, column=0, sticky="w", padx=20, pady=20)
        
        self.font_family = OptionsComboBox(self, "Font Family:", [str(family) for family in font.families()])
        self.font_family.grid(row=3, column=0, sticky="w", padx=20, pady=20)
        
        self.appearance_mode = OptionsComboBox(self, "Appearance Mode", ["System", "Light", "Dark"])
        self.appearance_mode.grid(row=4, column=0, sticky="w", padx=20, pady=20)
        
        self.bind("<Expose>", self.update_changes)
        
    def update_changes(self, event: Any = None):
        self.font_size.set_default_value(self.controller.app_settings["font_size"])
        self.text_wrapping.set_default_value(str(self.controller.app_settings["text_wrapping"]).capitalize())
        self.font_family.set_default_value(self.controller.app_settings["font_family"])
        self.appearance_mode.set_default_value(str(self.controller.app_settings["appearance_mode"]).capitalize())

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
        
        buttons = [["New File", controller.new_file],
                   ["Save File", controller.ask_save_file],
                   ["Open File", controller.ask_open_file],
                   ["Settings", lambda: controller.show_frame(Settings)]
                   ]
        self.topBar = TopBar(self, controller, buttons)
        self.topBar.grid(row=0, column=0, sticky="new")
        
        self.textBox_font = ctk.CTkFont(controller.app_settings["font_family"], controller.app_settings["font_size"])
        self.textBox = ctk.CTkTextbox(self, font=self.textBox_font, wrap=self.controller.app_settings["text_wrapping"])
        self.textBox.grid(row=1, column=0, sticky="nsew")
        
        self.textBox.bind("<Expose>", self.refresh)
        # self.textBox.bind("<Key>", self.check_file_changes)
        
        # Tkinter binding is CASE SENSITIVE.
        self.controller.non_case_sensitive_bind(self.textBox,
                                                ("Control", "s"),
                                                self.controller.ask_save_file)
        self.controller.non_case_sensitive_bind(self.textBox,
                                                ("Control", "o"),
                                                self.controller.ask_open_file)
        self.controller.non_case_sensitive_bind(self.textBox,
                                                ("Control", "n"),
                                                self.controller.new_file)
        
    
    def refresh(self, event):
        self.textBox_font.configure(family=self.controller.app_settings["font_family"],
                                    size=self.controller.app_settings["font_size"],)
        self.textBox.focus_set()
        self.textBox.configure(font=self.textBox_font,
                               wrap=self.controller.app_settings["text_wrapping"])
    
    #def check_file_changes(self, event):
    #    if self.controller.file_initial_content != self.textBox.get("0.0", "end").strip():
    #        self.controller.unsaved_changes = True
    #    else:
    #        self.controller.unsaved_changes = False
