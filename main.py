import customtkinter as ctk
from appPages import WrittingPage, Settings
from fileManagement import path
from pathlib import Path
import json

ctk.set_default_color_theme(path("assets/themes/app_theme.json"))

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.wm_title("MambaWritter")
        self.iconbitmap(path("assets/icons/MambaIcon.ico"))
        self.geometry("1280x720")
        self.minsize(720, 405)
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        settings_json_path = Path(path("cache/app_settings.json"))
        custom_settings_json_path = Path(path("cache/custom_app_settings.json"))
        if custom_settings_json_path.exists():
            with open(custom_settings_json_path, "r") as f:
                self.app_settings = json.loads(f.read())
        else:
            with open(settings_json_path, "r") as f:
                self.app_settings = json.loads(f.read())
            
        
        frame_list: tuple[ctk.CTkFrame] = [WrittingPage, Settings]
        self.frames = {}
        for F in frame_list:
            frame: ctk.CTkFrame = F(main_frame, self) # master (main_frame) and controller (App).
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(WrittingPage)

    def show_frame(self, frame_to_raise):
        frame: ctk.CTkFrame = self.frames[frame_to_raise]
        if hasattr(frame, 'on_show'):
            frame.on_show()
        frame.tkraise()

app = App()
app.mainloop()