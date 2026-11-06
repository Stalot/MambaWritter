import flet as ft
import os

FLET_APP_STORAGE_DATA = os.getenv("FLET_APP_STORAGE_DATA")
USER_DATA_PATH = os.path.join(FLET_APP_STORAGE_DATA, "user")

@ft.component
def EditorView():
    app_bar = ft.AppBar(
        leading=ft.Icon(ft.Icons.MENU),                            title=ft.TextField(
            "Untitled",
            border=ft.NoInputBorder(),
        ),
        actions=[
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
