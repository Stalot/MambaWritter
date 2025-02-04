import customtkinter as ctk

# ███████╗██╗     ███████╗███╗   ███╗███████╗███╗   ██╗████████╗███████╗
# ██╔════╝██║     ██╔════╝████╗ ████║██╔════╝████╗  ██║╚══██╔══╝██╔════╝
# █████╗  ██║     █████╗  ██╔████╔██║█████╗  ██╔██╗ ██║   ██║   ███████╗
# ██╔══╝  ██║     ██╔══╝  ██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║   ╚════██║
# ███████╗███████╗███████╗██║ ╚═╝ ██║███████╗██║ ╚████║   ██║   ███████║
# ╚══════╝╚══════╝╚══════╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝

class TransparentButton(ctk.CTkButton):
    def __init__(self,
                 master,
                 text = "Clean Button",
                 text_color = "Black",
                 text_color_on_hover = "green",
                 font = None,
                 command = None,
                 ):
        super().__init__(master, text=text, text_color=text_color, fg_color="transparent", font=font, hover=False, command=command)
        
        self.text_color_on_hover = text_color_on_hover
        
        self.default_config: dict = {"text": text,
                                     "text_color": text_color,
                                     "font": font,
                                    }
        
        self.bind("<Enter>", self.mouse_in)
        self.bind("<Leave>", self.mouse_out)
        
    def mouse_in(self, event):
        self.configure(True, text_color=self.text_color_on_hover)

    def mouse_out(self, event):
        self.configure(True, text_color=self.default_config["text_color"])

class TextBoxFrame(ctk.CTkFrame):
    def __init__(self,
                 master,
                 controller):
        super().__init__(master, fg_color="RED")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.textBox = ctk.CTkTextbox(self, corner_radius=0)
        self.textBox.grid(row=0, column=0, sticky="nsew")

class MenuButtonContainer(ctk.CTkFrame):
    def __init__(self,
                 master,
                 controller,
                 buttons: list | tuple = None,
                 vertical = False):
        super().__init__(master, fg_color="transparent")
        
        self.button_new_file = TransparentButton(self, "New file")
        self.button_new_file.grid(row=0, column=0)
        self.button_open_file = TransparentButton(self, "Open file")
        self.button_open_file.grid(row=0, column=1)

class DynamicButtonContainer(ctk.CTkFrame):
    def __init__(self,
                 master,
                 controller,
                 buttons: list | tuple = "Hello, world!",
                 vertical = False):
        super().__init__(master, fg_color="transparent")
        
        c = 0
        r = 0
        for button in buttons:
            new_button: TransparentButton = TransparentButton(self,
                                                              button.get("text"),
                                                              button.get("text_color"),
                                                              font=button.get("font"),
                                                              command=button.get("command"))
            new_button.grid(row=r, column=c, padx=20, pady=20)
            
            if vertical:
                r +=1
            else:
                c += 1

class TopBarButtons(ctk.CTkFrame):
    def __init__(self,
                 master,
                 controller):
        super().__init__(master)
        
        self.button_save_file = TransparentButton(self, "Save")
        self.button_app_settings = TransparentButton(self, "Settings")
        
        self.button_save_file.pack(side="left")
        self.button_app_settings.pack(side="left")