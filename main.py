from appPages import WrittingPage, Settings
from fileManagement import bundle_path, read_json, create_app_necessary_folders, iterate_file
from pathlib import Path
from typing import Final
from typing import Any, Dict, Optional, List, Type
from tkinter import messagebox
import customtkinter as ctk
import sys
import os

ctk.set_default_color_theme(bundle_path("assets/themes/app_theme.json"))

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.wm_title("MambaWritter")
        self.iconbitmap(bundle_path("assets/icons/MambaIcon.ico"))
        self.geometry("720x540")
        self.minsize(320, 180)
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        self.FOLDER_PATHS: Final[Dict[str, Path]] = create_app_necessary_folders()
        self.default_settings_json_path: Path = bundle_path("config/app_settings.json")
        self.custom_settings_json_path: Path = self.FOLDER_PATHS["appdata"] / "custom_app_settings.json"
        self.app_settings: dict = None
        if not self.custom_settings_json_path.exists():
            self.app_settings = read_json(self.default_settings_json_path)
        else:
            self.app_settings = read_json(self.custom_settings_json_path)
        
        self.device_logged_user_name: str = os.getlogin()
        self.user_files_directory: Path = self.FOLDER_PATHS["documents"]
        self.current_file: Optional[Path] = None
        self.unsaved_changes: bool = False
        self.file_initial_content: str = ""
        
        ctk.set_appearance_mode(self.app_settings["appearance_mode"])

        frame_list: List[Type[ctk.CTkFrame]] = [WrittingPage, Settings]
        self.frames = {}
        for F in frame_list:
            frame: ctk.CTkFrame = F(main_frame, self) # master (main_frame) and controller (App).
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.writtingpage_textbox: ctk.CTkTextbox = self.frames[WrittingPage].textBox
        
        self.show_frame(WrittingPage)
        self.open_file_on_start()
        
        self.protocol("WM_DELETE_WINDOW", self.closing_application)

    def show_frame(self, frame_to_raise):
        frame: ctk.CTkFrame = self.frames[frame_to_raise]
        if hasattr(frame, 'on_show'):
            frame.on_show()
        frame.tkraise()
    
    def open_file_on_start(self):
        """
        Opens a file when the user uses "Open with..." on Windows.
        """
        if len(sys.argv) > 1:
            try:
                filepath: Path = Path(sys.argv[1]).absolute() # The target file path
                self.wm_title(f"MambaWritter - {filepath.stem}")
                for line in iterate_file(filepath):
                    self.writtingpage_textbox.insert("end", line)
            except IOError as e:
                messagebox.showerror("Error",
                                     F"Failed to open file. {e}")
        self.file_initial_content = self.writtingpage_textbox.get("0.0", "end").strip()

    def closing_application(self):
        if self.unsaved_changes: # Checks if the current file has unsaved changes!
            if messagebox.askyesno("Unsaved Changes",
                                   f"Hey {self.device_logged_user_name}, your file has unsaved changes! Do you want to save your work before closing?"):
                if self.current_file.exists():
                    Path(self.current_file.absolute()).write_text(self.writtingpage_textbox.get('0.0', 'end').strip(), "utf-8")
                else:
                    self.ask_save_file()
        self.destroy() # Closes (destroy) window after everything

    def ask_save_file(self, event: Any = None):
        if not self.current_file.exists():
            file = ctk.filedialog.asksaveasfile(defaultextension="*.txt",
                                        filetypes=[("Text file", "*.txt"),
                                                    ("Markdown file", "*.md")],
                                        initialdir=self.user_files_directory,
                                        title="Save file")
            if file:
                self.current_file = Path(file.name)
                self.wm_title(f"MambaWritter - {self.current_file.stem}")
                
                Path(file.name).write_text(self.writtingpage_textbox.get('0.0', 'end').strip(), "utf-8")
        else:
            Path(self.current_file.absolute()).write_text(self.writtingpage_textbox.get('0.0', 'end').strip(), "utf-8")
        
        self.file_initial_content = self.writtingpage_textbox.get("0.0", "end").strip()
        self.unsaved_changes = False

    def ask_open_file(self):
        file = ctk.filedialog.askopenfile(defaultextension="*.txt",
                                   filetypes=[("Text file", "*.txt"),
                                                ("Markdown file", "*.md")],
                                   initialdir=self.user_files_directory,
                                   title="Open File")
        if file:
            self.writtingpage_textbox.delete("0.0", "end")
            self.current_file = Path(file.name)
            self.wm_title(f"MambaWritter - {self.current_file.stem}")
            
            for line in iterate_file(file.name):
                self.writtingpage_textbox.insert("end", line)
            self.file_initial_content = self.writtingpage_textbox.get("0.0", "end").strip()
            self.unsaved_changes = False

    def new_file(self):
        if self.unsaved_changes: # Checks if the current file has unsaved changes...
            if messagebox.askyesno("Unsaved Changes",
                                   f"{self.device_logged_user_name}, wait!\nYour file has unsaved changes, do you want to create a new file anyway?"):
                self.clear_textbox_content()
        else:
            self.clear_textbox_content()

    def clear_textbox_content(self):
        self.writtingpage_textbox.delete("0.0", "end")
        self.current_file = None
        self.file_initial_content = ""
        self.unsaved_changes = False
        self.wm_title("MambaWritter")

app = App()
app.mainloop()