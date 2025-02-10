import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.wm_title("MambaWritter")
        self.geometry("1280x720")
        self.minsize(720, 405)

app = App()
app.mainloop()