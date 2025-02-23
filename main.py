import customtkinter as ctk
from appPages import WrittingPage, Settings
from fileManagement import bundle_path, read_json, create_app_necessary_folders, iterate_file
from pathlib import Path
from typing import Final
import sys
from typing import Any, Dict, Optional

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
        self.app_settings: dict = read_json(self.default_settings_json_path) if not self.custom_settings_json_path.exists() else read_json(self.custom_settings_json_path)
        
        self.user_files_directory = self.FOLDER_PATHS["documents"]
        self.current_file: Optional[Path] = None
        
        ctk.set_appearance_mode(self.app_settings["appearance_mode"])

        from typing import List, Type
        frame_list: List[Type[ctk.CTkFrame]] = [WrittingPage, Settings]
        self.frames = {}
        for F in frame_list:
            frame: ctk.CTkFrame = F(main_frame, self) # master (main_frame) and controller (App).
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.writtingpage_textbox: ctk.CTkTextbox = self.frames[WrittingPage].textBox
        
        self.show_frame(WrittingPage)
        self.open_file_on_start()

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
            except Exception as e:
                self.writtingpage_textbox.insert("0.0", f"FATAL ERROR:\n{e}")

    def save_file_that_already_exists(self, event):
        if self.current_file:
            self.wm_title(f"MambaWritter - {self.current_file.stem}")
            Path(self.current_file.absolute()).write_text(self.writtingpage_textbox.get('0.0', 'end').strip(), "utf-8")

    def ask_save_file(self, event: Any = None):
        file = ctk.filedialog.asksaveasfile(defaultextension="*.txt",
                                     filetypes=[("Text file", "*.txt"),
                                                ("Markdown file", "*.md")],
                                     initialdir=self.user_files_directory,
                                     title="Save file")
        if file:
            self.current_file = Path(file.name)
            self.wm_title(f"MambaWritter - {self.current_file.stem}")
            
            Path(file.name).write_text(self.writtingpage_textbox.get('0.0', 'end').strip(), "utf-8")

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

    def new_file(self):
        self.writtingpage_textbox.delete("0.0", "end")
        self.current_file = None
        self.wm_title("MambaWritter")

app = App()
app.mainloop()