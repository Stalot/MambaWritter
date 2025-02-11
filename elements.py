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
        
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.textBox = ctk.CTkTextbox(self, corner_radius=0, wrap='word')
        self.textBox.grid(row=0, column=0, sticky="nsew")
        
        self.textBox.bind("<Expose>", self.refresh)
    
    def refresh(self, event):
        font_settings = self.controller.settings["textbox"]["font"]
        textbox_font = ctk.CTkFont(font_settings["family"], font_settings["size"], font_settings["weight"])
        self.textBox.configure(True, font=textbox_font)

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
                 buttons: tuple[dict] | list[dict]):
        super().__init__(master)
        
        id = 0
        for B in buttons:
            text = B.get("text") if B.get("text") != None else f"Button{id}"
            command = B.get("command")
            new_button = CustomButton(self, text=text, command=command)
            new_button.pack(side="left")
            id += 1

class idkbro(ctk.CTkFrame):
    def __init__(self,
                 master,
                 controller,
                 default_value: int = 32,
                 max_value: int = 64,
                 min_value: int = 16,
                 weight: int = 8
                 ):
        super().__init__(master)
        
        button_font = ctk.CTkFont("arial", 32, "bold")
        
        self.weight = weight
        self.max = max_value
        self.min = min_value
        self.value = default_value
        
        self.display = ctk.CTkLabel(self, text=str(self.value))
        self.button_plus = ctk.CTkButton(self, text="+", text_color="green", font=button_font, corner_radius=60, width=48, height=48, command=self.add)
        self.button_minus = ctk.CTkButton(self, text="-", text_color="red", font=button_font, corner_radius=60, width=48, height=48, command=self.subtract)
        
        
        self.button_plus.grid(row=0, column=0)
        self.button_minus.grid(row=0, column=2)
        self.display.grid(row=0, column=1)
    
    def add(self):
        result_value = self.value + self.weight
        self.value = result_value if result_value <= self.max else self.value
        self.display.configure(True, text=self.value)
        

    def subtract(self):
        result_value = self.value - self.weight
        self.value = result_value if result_value >= self.min else self.value
        self.display.configure(True, text=self.value)
    
    def current_value(self):
        return self.value
        
class Footer(ctk.CTkFrame):
    def __init__(self,
                 master):
        super().__init__(master)
        
        label = ctk.CTkLabel(self, text="Open source program, MIT Licence Copyright (c) 2025 Orly Neto")
        
        label.grid(row=0, column=0, padx=10)