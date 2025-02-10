import customtkinter as ctk
from pathlib import Path
from PIL import Image

# ███████╗██╗     ███████╗███╗   ███╗███████╗███╗   ██╗████████╗███████╗
# ██╔════╝██║     ██╔════╝████╗ ████║██╔════╝████╗  ██║╚══██╔══╝██╔════╝
# █████╗  ██║     █████╗  ██╔████╔██║█████╗  ██╔██╗ ██║   ██║   ███████╗
# ██╔══╝  ██║     ██╔══╝  ██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║   ╚════██║
# ███████╗███████╗███████╗██║ ╚═╝ ██║███████╗██║ ╚████║   ██║   ███████║
# ╚══════╝╚══════╝╚══════╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝

class FileRow(ctk.CTkFrame):
    def __init__(self,
                 master,
                 controller,
                 filepath: Path,
                 command):
        super().__init__(master)
        
        self.controller = controller
        
        fileicon = ctk.CTkImage(Image.open("assets/icons/FileIcon.png"), size=(32, 32))
        
        self.filename = filepath.name
        #self.filepath = filepath.absolute()
        
        self.file = ctk.CTkButton(self, image=fileicon, text=self.filename, font=ctk.CTkFont("arial", 16), anchor="w", command=lambda: command(filepath.absolute()))
        self.file.grid(row=0, column=0, sticky="ew")

class UserFiles(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        
        self.title = ctk.CTkLabel(self, text="User Files", font=ctk.CTkFont("arial", 24))
        self.title.grid(row=0, column=0, pady=(0, 16), sticky="w")
        
        r = 1
        for file in Path("C:/Users/Junior/Documents/MambaWritter").glob("*"):
            file_row = FileRow(self, controller, file, master.open_file)
            file_row.grid(row=r, column=0, sticky="w")
            r += 1

if __name__ == "__main__":
    for file in Path("C:/Users/Junior/Documents/MambaWritter").glob("*"):
        print(file.absolute().name)