import customtkinter as ctk
from tabs import AppMenu, WrittingPage
from fileManagement import find_internal_folder_in_cwd
import json
from pathlib import Path

_internal_folder_path: Path | None = find_internal_folder_in_cwd()

settings_path = _internal_folder_path.joinpath("cache/settings.json") if _internal_folder_path else Path.cwd().joinpath("cache/settings.json")
theme_path = _internal_folder_path.joinpath("assets/theme/theme.json") if _internal_folder_path else Path.cwd().joinpath("assets/theme/theme.json")

ctk.set_appearance_mode("light")
ctk.set_default_color_theme(theme_path)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.wm_title("MambaWritter")
        self.geometry("1280x720")
        self.minsize(720, 405)
        
        with open(settings_path, "r") as f:            
            self.settings: dict = json.loads(f.read())
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(side='top', fill='both', expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (AppMenu, WrittingPage):
            frame = F(main_frame, self)
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(AppMenu)

    def show_frame(self, frame_to_raise):
        frame: ctk.CTkFrame = self.frames[frame_to_raise]
        if hasattr(frame, 'on_show'):
            frame.on_show()
        frame.tkraise()

app = App()
app.mainloop()