import customtkinter as ctk
from appPages import WrittingPage, Settings
from fileManagement import bundle_path, read_json
from pathlib import Path

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
        
        self.settings_json_path: Path = bundle_path("cache/app_settings.json")
        self.custom_settings_json_path: Path = bundle_path("cache/custom_app_settings.json")
        self.app_settings: dict = read_json(self.settings_json_path) if not self.custom_settings_json_path.exists() else read_json(self.custom_settings_json_path)
        
        ctk.set_appearance_mode(self.app_settings["appearance_mode"])

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