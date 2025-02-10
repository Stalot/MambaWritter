import customtkinter as ctk
from appPages import Menu, WrittingPage

ctk.set_default_color_theme("assets/themes/app_theme.json")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.wm_title("MambaWritter")
        self.iconbitmap("assets/icons/MambaIcon.ico")
        self.geometry("1280x720")
        self.minsize(720, 405)
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        frame_list: tuple[ctk.CTkFrame] = (Menu, WrittingPage)
        self.frames = {}
        for F in frame_list:
            frame: ctk.CTkFrame = F(main_frame, self) # master (main_frame) and controller (App).
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Menu)
        print(self.frames)

    def show_frame(self, frame_to_raise):
        frame: ctk.CTkFrame = self.frames[frame_to_raise]
        if hasattr(frame, 'on_show'):
            frame.on_show()
        frame.tkraise()

app = App()
app.mainloop()