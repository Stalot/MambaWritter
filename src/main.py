import flet as ft
import os
from pathlib import Path

FLET_APP_STORAGE_DATA: Path = Path(os.getenv("FLET_APP_STORAGE_DATA"))
DEFAULT_USER_DATA_PATH: Path = FLET_APP_STORAGE_DATA / "user"

@ft.component
def EditorView():
    textbox_value, set_textbox_value = ft.use_state("")
    app_bar_title, set_app_bar_title = ft.use_state("Untitled.txt")

    async def save_file():
        path: Path = USER_DATA_PATH / app_bar_title
        if path.exists():
            with open(path, "w") as file:
                file.write(textbox_value)

    async def save_file_as(e):
        file_picker = ft.FilePicker()
        encoded: bytes = textbox_value.encode("utf-8")
        await file_picker.save_file(
            file_name=app_bar_title,
            src_bytes=encoded if encoded else b" ",
        )

    async def handle_textbox_change(e):
        set_textbox_value(e.control.value)
        await save_file()

    app_bar = ft.AppBar(
        leading=ft.PopupMenuButton(
            icon=ft.Icons.MENU,
            items=[
                ft.PopupMenuItem(
                    "Save as",
                    on_click=save_file_as,
                ),
                ft.PopupMenuItem("Open file"),
                ft.PopupMenuItem("Settings"),
            ]
        ),
        title=ft.Text(f"{app_bar_title}"),
        actions=[
            ft.IconButton(ft.Icons.MORE_VERT),
        ],                                                     )

    textbox = ft.TextField(
        expand=True,
        value=textbox_value,
        hint_text="Write your ideas here...",
        multiline=True,
        border=ft.NoInputBorder(),
        on_change=handle_textbox_change,
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
    this_view = ft.View(
        route="/",
        appbar=app_bar,
        controls=content,
    )
    return this_view

@ft.component
def App():
    router = ft.Router(
        [
            ft.Route(
                component=EditorView,
            ),
        ],
        manage_views=True,
    )
    return router

if __name__ == "__main__":
    ft.run(lambda page: page.render_views(App))
