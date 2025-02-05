import customtkinter as ctk
from elements import DynamicButtonContainer, TextBoxFrame, TopBarButtons, Footer

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
        
        button_new_file: dict = {"text": "Write",
                                 "hover_color": "white",
                                 "command": lambda: self.controller.show_frame(WrittingPage),
                                 "font": self.font_button}
        button_open_file: dict = {"text": "Settings",
                                 "hover_color": "white",
                                 "command": lambda: self.controller.show_frame(WrittingPage),
                                 "font": self.font_button}
        
        self.container = DynamicButtonContainer(self, controller, (button_new_file, button_open_file), vertical=False)
        self.container.grid(row=1, column=0, sticky="n")
        
        self.footer = Footer(self)
        self.footer.grid(row=999, column=0, sticky="ew")
    
    def bazinga(self):
        print("BAZINGAAAAA!!!")

class WrittingPage(ctk.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        buttons: tuple[dict] = (
            {"text": "Menu", "command": lambda c=controller: c.show_frame(AppMenu)}, 
            {"text": "Save", "command": self.save_file},
            {"text": "Open", "command": self.load_file}
            )
        
        self.topbar = TopBarButtons(self, controller, buttons)
        self.topbar.grid(row=0, column=0, sticky="ew")
        
        self.box = TextBoxFrame(self, controller)
        self.box.grid(row=1, column=0, sticky="nsew")

    def save_file(self):
        print("Saving file...")
        filename = ctk.filedialog.asksaveasfilename(initialdir='/', title='Save file', filetypes=[('Text file', '*.txt')])
        with open(f'{filename}.txt', 'w', encoding='utf-8') as f:
            text: str = str(self.box.textBox.get('0.0', 'end')).strip()
            f.write(text)

    def load_file(self):
        print("Loading file...")
        filename = ctk.filedialog.askopenfilename(initialdir='/', title='Load file', filetypes=[('Text file', '*.txt')])
        with open(filename, 'r', encoding='utf-8') as f:
            text: str = str(f.read()).strip()
        
        self.box.textBox.delete("0.0", "end")
        self.box.textBox.insert("0.0", text)