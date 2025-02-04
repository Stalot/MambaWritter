import customtkinter as ctk
from elements import TransparentButton, MenuButtonContainer, DynamicButtonContainer, TextBoxFrame, TopBarButtons

# ████████╗ █████╗ ██████╗ ███████╗
# ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝
#    ██║   ███████║██████╔╝███████╗
#    ██║   ██╔══██║██╔══██╗╚════██║
#    ██║   ██║  ██║██████╔╝███████║
#    ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚══════╝

class AppMenu(ctk.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        
        self.font_title = ctk.CTkFont("Arial", 100, "bold", "roman")
        self.font_button = ctk.CTkFont("Times New Roman", 32)
        
        self.controller = controller
        
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.title = ctk.CTkLabel(self, text="MambaWritter", font=self.font_title)
        self.title.grid(row=0, column=0)
        
        button_new_file: dict = {"text": "Write a new file",
                                 "text_color": "black",
                                 "command": self.create_new_file,
                                 "font": self.font_button}
        button_open_file: dict = {"text": "Open a file",
                                 "text_color": "black",
                                 "command": self.bazinga,
                                 "font": self.font_button}
        
        self.container = DynamicButtonContainer(self, controller, (button_new_file, button_open_file), vertical=True)
        self.container.grid(row=1, column=0)
    
    def bazinga(self):
        print("BAZINGAAAAA!!!")

    def create_new_file(self):
        self.controller.show_frame(AppMenu2)

class AppMenu2(ctk.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        
        self.controller = controller
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.topbar = TopBarButtons(self, None)
        self.topbar.grid(row=0, column=0, sticky="ew")
        
        self.box = TextBoxFrame(self, None)
        self.box.grid(row=1, column=0, sticky="nsew")