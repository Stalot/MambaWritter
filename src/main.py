import flet as ft
from pathlib import Path
import os

FLET_APP_STORAGE_DATA = os.getenv("FLET_APP_STORAGE_DATA")
USER_DATA_PATH = FLET_APP_STORAGE_DATA+"/user"

@ft.component
def HomeView():
    app_bar = ft.AppBar(
        title=ft.Text("Your files."),
    )
    ft.context.page.appbar = app_bar
    ft.context.page.update()

    def get_user_files():
        files = []
        for f in os.scandir(USER_DATA_PATH):
            files.append({
                "file_name": f.name,
                "path": f.path
            })
        return files

    async def open_file(e):
        ft.context.page.file_path = e.control.data
        await ft.context.page.push_route("/editor")

    content = ft.Column(
        controls=[
            ft.TextButton(
                file["file_name"],
                on_click=open_file,
                data=file["path"],
            ) for file in get_user_files()
        ]
    )
    return content

def EditorView():
    app_bar = ft.AppBar(
        leading=ft.Icon(ft.Icons.MENU),                            title=ft.Text("Untitled.txt"),
        actions=[
            ft.IconButton(
                ft.Icons.SEARCH,
                on_click=lambda e: ft.context.page.navigate("/")
            ),
            ft.IconButton(ft.Icons.MORE_VERT),
        ],                                                     )
    ft.context.page.appbar = app_bar
    ft.context.page.update()

    def default_text():
        text: str = ""
        with open(ft.context.page.file_path, "r") as f:
            text = f.read()
        return text

    textbox = ft.TextField(
        value=default_text(),
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
                    component=HomeView
                ),
                ft.Route(
                    path="editor",
                    component=EditorView,
                ),
            ]
        ),
    )

if __name__ == "__main__":
    ft.run(lambda page: page.render(App))
