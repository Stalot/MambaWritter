import customtkinter as ctk

# ███████╗██╗     ███████╗███╗   ███╗███████╗███╗   ██╗████████╗███████╗
# ██╔════╝██║     ██╔════╝████╗ ████║██╔════╝████╗  ██║╚══██╔══╝██╔════╝
# █████╗  ██║     █████╗  ██╔████╔██║█████╗  ██╔██╗ ██║   ██║   ███████╗
# ██╔══╝  ██║     ██╔══╝  ██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║   ╚════██║
# ███████╗███████╗███████╗██║ ╚═╝ ██║███████╗██║ ╚████║   ██║   ███████║
# ╚══════╝╚══════╝╚══════╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝

class CustomButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.hover_color = kwargs["hover_color"] if kwargs.get("hover_color") != None else "white"

        self.bind("<Enter>", self.mouse_in)
        self.bind("<Leave>", self.mouse_out)
        
    def mouse_in(self, event):
        self.configure(True, fg_color=self.hover_color)

    def mouse_out(self, event):
        self.configure(True, fg_color="white")

class TextBoxFrame(ctk.CTkFrame):
    def __init__(self,
                 master,
                 controller):
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        font_settings = controller.settings["textbox"]["font"]
        textbox_font = ctk.CTkFont(font_settings["family"], font_settings["size"], font_settings["weight"])
        
        self.textBox = ctk.CTkTextbox(self, corner_radius=0, font=textbox_font, wrap='word')
        self.textBox.grid(row=0, column=0, sticky="nsew")

class DynamicButtonContainer(ctk.CTkFrame):
    def __init__(self,
                 master,
                 controller,
                 buttons: list[dict] | tuple[dict] = [{"text": "Hello, world!", "command": None}],
                 vertical = False):
        super().__init__(master, fg_color="transparent")

        c: int = 0
        r: int = 0
        for B in buttons:
            text = B.get("text") if B.get("text") != None else "Button"
            font = B.get("font")
            command = B.get("command")
            new_button = CustomButton(self, text=text, font=font, hover_color="white", command=command)          
            
            if vertical:
                new_button.grid(row=r, column=0, padx=5, pady=10)
            else:
                new_button.grid(row=0, column=c, padx=10, pady=5)
            
            r += 1
            c += 1

class TopBarButtons(ctk.CTkFrame):
    def __init__(self,
                 master,
                 controller,
                 buttons: tuple[dict]):
        super().__init__(master)
        
        id = 0
        for B in buttons:
            text = B.get("text") if B.get("text") != None else f"Button{id}"
            command = B.get("command")
            new_button = CustomButton(self, text=text, command=command)
            new_button.pack(side="left")
            id += 1

class Footer(ctk.CTkFrame):
    def __init__(self,
                 master):
        super().__init__(master)
        
        label = ctk.CTkLabel(self, text="Open source program, MIT Licence Copyright (c) 2025 Orly Neto")
        
        label.grid(row=0, column=0, padx=10)