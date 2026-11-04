import flet as ft
from pathlib import Path
import os

FLET_APP_STORAGE_DATA = os.getenv("FLET_APP_STORAGE_DATA")
USER_DATA_PATH = os.path.join(FLET_APP_STORAGE_DATA, "user")

class UserFiles(ft.Container):
    def __init__(self):
        self.files = ft.ListView(
            controls=[
                ft.Text("No files here...")
            ]
        )
        self.reload()
        super().__init__(
            content=self.files
        )

    def reload(self):
        def file_template(file_data):
            return ft.Text(file_data.name)
        data_found = []
        for item in self.get_dir_content(USER_DATA_PATH):
            if item:
                data_found.append(file_template(item))
        if data_found:
            self.files.controls = data_found

    def get_dir_content(self, path):
        return os.scandir(path)

@ft.component
def FileManagerView():
    app_bar = ft.AppBar(
        #leading=ft.Icon(ft.Icons.MENU),
        title=ft.Text("File Manager"),
        actions=[
            ft.IconButton(
                ft.Icons.ADD,
                on_click=lambda e: ft.context.page.navigate("/")
            ),
        ],
    )
    ft.context.page.appbar = app_bar
    ft.context.page.update()
    return UserFiles()

@ft.component
def EditorView():
    app_bar = ft.AppBar(
        leading=ft.Icon(ft.Icons.MENU),                            title=ft.Text("Untitled.txt"),
        actions=[
            ft.IconButton(
                ft.Icons.SEARCH,
                on_click=lambda e: ft.context.page.navigate("/test/435")
            ),
            ft.IconButton(ft.Icons.MORE_VERT),
        ],                                                     )
    ft.context.page.appbar = app_bar

    #def default_text():
    #    text: str = ""
    #    with open(ft.context.page.file_path, "r") as f:
    #        text = f.read()
    #    return text

    textbox = ft.TextField(
            #value=default_text(),
        expand=True,
        hint_text="Write your ideas here...",
        multiline=True,
        border=ft.NoInputBorder(),
    )

    content = ft.Column(
        expand=True,
        controls=[
            textbox,
        ]
    )
    return content

@ft.component
def App():
    ft.context.page.padding=20
    return ft.SafeArea(
        expand=True,
        content=ft.Router(
            [
                ft.Route(
                    index=True,
                    component=EditorView
                ),
                ft.Route(
                    path="test/:id",
                    component=FileManagerView,
                ),
            ]
        ),
    )

if __name__ == "__main__":
    ft.run(lambda page: page.render(App))
