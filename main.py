import customtkinter as ctk
from tabs import AppMenu, AppMenu2

ctk.set_appearance_mode("light")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.wm_title("MambaWritter")
        self.geometry("960x540")
        self.attributes("-fullscreen", True)
        
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(side='top', fill='both', expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (AppMenu, AppMenu2):
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