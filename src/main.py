import flet as ft
import flet_permission_handler as ftph
import os
from pathlib import Path

FLET_APP_STORAGE_DATA: Path = Path(os.getenv("FLET_APP_STORAGE_DATA"))
DEFAULT_USER_DATA_PATH: Path = FLET_APP_STORAGE_DATA / "user"

# status = await ph.get_status(fph.Permission.MICROPHONE)

@ft.component
def AppStartupView():
    ft.context.page.navigate("setup/android")
    return ft.View(
        route="/",
    )

@ft.component
def AndroidSetupView():
    finish_button_disabled, set_finish_button_disabled = ft.use_state(True)
    current_storage_location, set_current_storage_location = ft.use_state(DEFAULT_USER_DATA_PATH)

    ph = ftph.PermissionHandler()

    async def request_external_storage(e):
        await ph.request(ftph.Permission.MANAGE_EXTERNAL_STORAGE),

    async def ask_folder_location(e):
        picker = ft.FilePicker()
        path = await picker.get_directory_path()

        set_current_storage_location(path)

    def option_card(
        title: str,
        description: str,
        actions: list,
    ):
        return ft.Container(
            border=ft.Border.all(2, ft.Colors.GREY),
            border_radius=ft.BorderRadius.all(4),
            padding=8,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Text(
                        title,
                        theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
                    ),
                    ft.Text(description),
                    ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    action
                                ]
                            ) for action in actions
                        ]
                    )
                ]
            )
        )

    content = ft.SafeArea(
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                ft.Text(
                    "Android setup",
                    theme_style=ft.TextThemeStyle.HEADLINE_LARGE,
                ),
                ft.Text(
                    "Necessary steps so MambaWritter works correctly.",
                    theme_style=ft.TextThemeStyle.BODY_LARGE,
                ),
                ft.ListView(
                    expand=True,
                    spacing=16,
                    controls=[
                        option_card(
                            title="Storage",
                            description=f"Select a folder where MambaWritter will keep all your files.\n\nCurrent: '{current_storage_location}'",
                            actions=[
                                ft.TextButton(
                                    expand=True,
                                    content="Select folder",
                                    on_click=ask_folder_location,
                                )
                            ]
                        ),
                        option_card(
                            title="Manage External Storage",
                            description="Necessary for saving and opening files.",
                            actions=[
                                ft.TextButton(
                                    expand=True,
                                    content="Grant permission",
                                    on_click=request_external_storage,
                                )
                            ]
                        )
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.TextButton(
                            expand=True,
                            content="Finish setup",
                            on_click=lambda: ft.context.page.navigate("/editor"),
                            disabled=finish_button_disabled,
                        )
                    ]
                )
            ]
        )
    )

    this_view = ft.View(
        route="setup/android",
        padding=20,
        controls=[
            content
        ]
    )
    return this_view

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
        route="/editor",
        appbar=app_bar,
        controls=content,
    )
    return this_view

@ft.component
def App():
    router = ft.Router(
        [
            ft.Route(
                path="/",
                component=AppStartupView,
                children=[
                    ft.Route(
                        path="setup/android",
                        component=AndroidSetupView,
                    )
                ]
            ),
            ft.Route(
                path="/editor",
                component=EditorView,
            ),
        ],
        manage_views=True,
    )
    return router

if __name__ == "__main__":
    ft.run(lambda page: page.render_views(App))
