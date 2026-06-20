import flet as ft
import os
from pathlib import Path

APP_DATA_PATH: Path = Path(os.getenv("FLET_APP_STORAGE_DATA"))
APP_DATA_TEMP_PATH: Path = Path(os.getenv("FLET_APP_STORAGE_TEMP"))

APP_DATA_PATH.mkdir(parents=True, exist_ok=True)
APP_DATA_TEMP_PATH.mkdir(parents=True, exist_ok=True)

async def main(page: ft.Page):
    page.padding = 4
    page.spacing = 2

    def home_view() -> ft.View:
        async def goto_editor():
            await page.push_route("/editor")
        async def new_file(e):
            page.session.store.set("textfield_default_value", "")
            await goto_editor()
        async def open_file(e):
            file_path: Path = e.control.data
            with open(file_path, "r") as f:
                content: str = f.read()
            page.session.store.set("textfield_default_value", content)
            await goto_editor()

        def user_files():
            path = APP_DATA_PATH / "user"
            return [file for file in path.glob("*")]

        appBar = ft.AppBar(
            title="MambaWritter",
            actions=[
                ft.TextButton(
                    "New file",
                    on_click=new_file
                ),
            ],
        )
        view = ft.View(
            route="/",
            controls=[
                ft.SafeArea(
                    content=ft.Column(
                        controls=[
                            ft.TextButton(
                                file.name,
                                data=file.resolve(),
                                on_click=open_file
                            ) for file in user_files()
                        ]
                    )
                )
            ]
        )
        view.appbar = appBar
        return view

    def editor_view() -> ft.View:
        def default_value() -> str:
            return page.session.store.get("textfield_default_value")

        app_bar = ft.AppBar()
        view = ft.View(
            route="/editor",
            controls=[
                ft.SafeArea(
                    expand=True,
                    content=ft.Column(
                        expand=True,
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.TextField(
                                        expand=True,
                                        border=ft.InputBorder.NONE,
                                        hint_text="Title",
                                    ),
                                ],
                            ),
                            ft.TextField(
                                expand=True,
                                border=ft.InputBorder.NONE,
                                text_size=16,
                                multiline=True,
                                hint_text="...",
                                value=default_value()
                            )
                        ]
                    )
                )
            ]
        )
        view.appbar = app_bar
        return view

    def route_change():
        page.views.clear()
        page.views.append(home_view())
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
