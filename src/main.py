import flet as ft
import os
from pathlib import Path

APP_DATA_PATH = os.getenv("FLET_APP_STORAGE_DATA")
APP_DATA_TEMP_PATH = os.getenv("FLET_APP_STORAGE_TEMP")
USER_FILES_PATH = Path.home() / "storage/shared/Documents/MambaWritter"

USER_FILES_PATH.mkdir(parents=True, exist_ok=True)

def home_view(page: ft.Page) -> ft.View:
    async def new_file(e):                                         await page.push_route("/editor")

    app_bar = ft.AppBar(
        title="My Files",
        actions=[
            ft.IconButton(ft.Icons.ADD,
                          on_click=new_file)
        ]
    )
    view = ft.View(
        route="/",
        controls=[]
    )
    view.appbar = app_bar
    return view

def editor_view() -> ft.View:
    def save_changes(e):
        with open(USER_FILES_PATH / "file.txt", "w") as f:
            f.write(text_field.value)
    app_bar = ft.AppBar(
            title="MambaWritter",
            )
    text_field = ft.TextField(                                     expand=True,
        border=ft.InputBorder.NONE,                                hint_text="Type here...",
        text_size=16,                                              multiline=True,
        on_change=save_changes,
    )
    container = ft.Container(
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                text_field                                             ],
        ),                                                     )

    view = ft.View(
        route = "/editor",
        controls=[
            container
        ]
    )
    view.appbar = app_bar
    return view


def main(page: ft.Page):
    page.padding = 4
    page.spacing = 2

    def route_change():
        page.views.clear()
        page.views.append(home_view(page))
        match page.route:
            case "/editor":
                page.views.append(editor_view())

    async def view_pop(e):
        if e.view is not None:
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change()

if __name__ == "__main__":
    ft.run(main)
