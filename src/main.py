import flet as ft
import os
from pathlib import Path

FLET_APP_STORAGE_DATA = Path(os.getenv("FLET_APP_STORAGE_DATA"))
USER_DATA_PATH = FLET_APP_STORAGE_DATA / "user"

@ft.component
def EditorView():
    show_rename_file_dialog, set_show_rename_file_dialog = ft.use_state(False)
    textbox_value, set_textbox_value = ft.use_state("")

    ft.use_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text("Renaming file"),
            content=ft.TextField(
                hint_text="ex: ToDo.txt"
            ),
            actions=[
                ft.TextButton(
                    "Confirm",
                    on_click=lambda: set_show_rename_file_dialog(False)
                ),
                ft.TextButton(
                    "Nevermind",
                    on_click=lambda: set_show_rename_file_dialog(False)
                ),
            ],
        ) if show_rename_file_dialog else None
    )

    async def save_file(e):
        title: str = app_bar.title.value
        path: Path = USER_DATA_PATH / title
        #with open(path, "w") as file:
        #    file.write(textbox.value)
    # Bind to the AlertDialog later
    #async def rename_file(e):
    #    title: str = app_bar.title.value
    #    old_path = Path(USER_DATA_PATH / title)
    #    set_show_rename_file_dialog(True)
    async def handle_textbox_change(e):
        set_textbox_value(e.control.value)

    app_bar = ft.AppBar(
        leading=ft.PopupMenuButton(
            icon=ft.Icons.MENU,
            items=[
                ft.PopupMenuItem(
                    "Rename file",
                    on_click=lambda: set_show_rename_file_dialog(True),
                ),
                ft.PopupMenuItem("Save as"),
                ft.PopupMenuItem("Open file"),
                ft.PopupMenuItem("Settings"),
            ]
        ),
        title=ft.Text("Untitled"),
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
