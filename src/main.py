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
        title=ft.Text("File Manager"),
        actions=[
            ft.IconButton(
                ft.Icons.ADD,
                on_click=lambda e: ft.context.page.navigate("/")
            ),
        ],
    )
    content = ft.SafeArea(
        expand=True,
        content=UserFiles()
    )
    return ft.View(
        route="/file-manager",
        appbar=app_bar,
        controls=content,
    )

@ft.component
def EditorView():
    app_bar = ft.AppBar(
        leading=ft.Icon(ft.Icons.MENU),                            title=ft.Text("Untitled.txt"),
        actions=[
            ft.IconButton(
                ft.Icons.SEARCH,
                on_click=lambda e: ft.context.page.navigate("/file-manager")
            ),
            ft.IconButton(ft.Icons.MORE_VERT),
        ],                                                     )

    textbox = ft.TextField(
        expand=True,
        hint_text="Write your ideas here...",
        multiline=True,
        border=ft.NoInputBorder(),
    )

    content = ft.SafeArea(
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                textbox,
            ]
        )
    )
    return ft.View(
        route="/",
        appbar=app_bar,
        controls=content,
    )

@ft.component
def App():
    #ft.context.page.padding=20
    router = ft.Router(
        [
            ft.Route(
                component=EditorView,
                children=[
                    ft.Route(
                        path="file-manager",
                        component=FileManagerView,
                    ),
                ],
            ),
        ],
        manage_views=True,
    )
    return router

if __name__ == "__main__":
    ft.run(lambda page: page.render_views(App))
