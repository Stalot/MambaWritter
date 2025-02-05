import customtkinter as ctk
from tabs import AppMenu, WrittingPage, SettingsTab
from fileManagement import find_internal_folder_in_cwd
import json
from pathlib import Path

_internal_folder_path: Path | None = find_internal_folder_in_cwd()

assets_folder  = _internal_folder_path.joinpath("assets") if _internal_folder_path else Path.cwd().joinpath("assets")
cache_folder = _internal_folder_path.joinpath("cache") if _internal_folder_path else Path.cwd().joinpath("cache")

theme_filepath = assets_folder.joinpath("theme/theme.json")
appicon_filepath = assets_folder.joinpath("MambaLogo.ico")


ctk.set_appearance_mode("light")
ctk.set_default_color_theme(theme_filepath)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.wm_title("MambaWritter")
        self.iconbitmap(appicon_filepath)
        self.geometry("1280x720")
        self.minsize(720, 405)
        
        self.default_settings_filepath = cache_folder.joinpath("default_settings.json")
        self.settings_filepath = cache_folder.joinpath("settings.json")
        
        self.settings: dict = self.read_settings()
            
        self.user = Path.home()
        self.user_files_folderpath: Path = self.user.joinpath("Documents", "MambaWritter")
        if not self.user_files_folderpath.exists():
            self.user_files_folderpath.mkdir()
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(side='top', fill='both', expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (AppMenu, WrittingPage, SettingsTab):
            frame = F(main_frame, self)
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(AppMenu)

    def show_frame(self, frame_to_raise):
        frame: ctk.CTkFrame = self.frames[frame_to_raise]
        if hasattr(frame, 'on_show'):
            frame.on_show()
            
        self.read_settings()
        
        frame.tkraise()
    
    def read_settings(self):
        path = self.settings_filepath if self.settings_filepath.exists() else self.default_settings_filepath
        with open(path, "r") as f:
            self.settings: dict = json.loads(f.read())
        return self.settings

app = App()
app.mainloop()