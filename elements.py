import customtkinter as ctk

# ███████╗██╗     ███████╗███╗   ███╗███████╗███╗   ██╗████████╗███████╗
# ██╔════╝██║     ██╔════╝████╗ ████║██╔════╝████╗  ██║╚══██╔══╝██╔════╝
# █████╗  ██║     █████╗  ██╔████╔██║█████╗  ██╔██╗ ██║   ██║   ███████╗
# ██╔══╝  ██║     ██╔══╝  ██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║   ╚════██║
# ███████╗███████╗███████╗██║ ╚═╝ ██║███████╗██║ ╚████║   ██║   ███████║
# ╚══════╝╚══════╝╚══════╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝

class OptionsComboBox(ctk.CTkFrame):
    def __init__(self,
                 master,
                 title: str = "Option",
                 options: list[str] = ["Value-1", "Value-2", "Value-3"]):
        super().__init__(master)
        
        self.title = ctk.CTkLabel(self, text=title, anchor="w")
        self.optionsBox = ctk.CTkComboBox(self, values=[item for item in options], dropdown_hover_color=("gray84", "gray14"))
        
        self.title.grid(row=0, column=0, sticky="ew")
        self.optionsBox.grid(row=1, column=0)
    
    def current_selection(self) -> str:
        return str(self.optionsBox.get())
    
    def set_default_value(self, value: str) -> None:
        self.optionsBox.set(str(value))

class TopBar(ctk.CTkFrame):
    def __init__(self,
                 master,
                 controller,
                 buttons: list[list]):
        super().__init__(master)
        
        c = 0
        for b in buttons:
            new_button = ctk.CTkButton(self, text=b[0], command=b[1], hover=False)
            new_button.grid(row=0, column=c)
            c += 1