import flet as ft
import os
from pathlib import Path
import asyncio

APP_DATA_PATH: Path = Path(os.getenv("FLET_APP_STORAGE_DATA"))
APP_DATA_TEMP_PATH: Path = Path(os.getenv("FLET_APP_STORAGE_TEMP"))
USER_DIR: Path = APP_DATA_PATH / "user"

APP_DATA_PATH.mkdir(parents=True, exist_ok=True)
APP_DATA_TEMP_PATH.mkdir(parents=True, exist_ok=True)
USER_DIR.mkdir(parents=True, exist_ok=True)

async def main(page: ft.Page):
    page.padding = 4
    page.spacing = 2

    page.editor_data: dict[str, str] = {
        "file_name": "",
        "text": ""
    }

    def home_view() -> ft.View:
        async def event_new_file(e):
            page.editor_data["file_name"] = ""
            page.editor_data["text"] = ""
            await page.push_route("/editor")
        async def event_open_file(e):
            file_path: Path = e.control.data
            with open(file_path, "r") as f:
                text: str = f.read()
            page.editor_data["file_name"] = file_path.stem
            page.editor_data["text"] = text
            await page.push_route("/editor")
        async def event_pop_file(e):
            def delete(file_path: Path):
               file_path.unlink(missing_ok=True)
            text_button = e.control
            text_button.disabled = True
            event_data: dict[str, ft.Row | Path] = e.control.data
            row: ft.Row = event_data["row"]
            file_path: Path = event_data["file_path"]
            await asyncio.to_thread(delete, file_path)
            user_files.controls.remove(row)
            
        user_files: ft.ListView = ft.ListView(
            spacing=10,
            padding=20,
            expand=True,
        )
        for file in USER_DIR.glob("*"):
            row = ft.Row()
            row.controls.append(
                ft.Container(
                    content=ft.TextButton(
                        file.name,
                        data=file.resolve(),
                        on_click=event_open_file
                    )
                )
            )
            row.controls.append(
                ft.Container(
                    alignment=ft.Alignment.CENTER_RIGHT,
                    content=ft.TextButton(
                        "Delete",
                        data={
                            "row": row,
                            "file_path": Path(file.resolve())
                        },
                        on_click=event_pop_file
                    )
                )
            )
            user_files.controls.append(row)

        appBar = ft.AppBar(
            title="MambaWritter",
            actions=[
                ft.TextButton(
                    "New file",
                    on_click=event_new_file
                ),
            ],
        )

        view = ft.View(
            route="/",
            controls=[
                ft.SafeArea(
                    expand=True,
                    content=user_files
                ),
            ]
        )
        view.appbar = appBar
        return view

    def editor_view() -> ft.View:
        text_box = ft.TextField(
            expand=True,
            border=ft.InputBorder.NONE,
            text_size=16,
            multiline=True,
            hint_text="...",
            value=page.editor_data["text"]
        )
        file_title = ft.TextField(
            expand=True,
            border=ft.InputBorder.NONE,
            text_size=16,
            hint_text="Title",
            value=page.editor_data["file_name"]
        )
        editor = ft.Container(
            expand=True,
            alignment=ft.Alignment.TOP_LEFT,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Row(
                        controls=[
                            file_title,
                        ]
                    ),
                    text_box
                ]
            )
        )
        app_bar: ft.AppBar = ft.AppBar()
        view = ft.View(
            route="/editor",
            controls=[
                ft.SafeArea(
                    expand=True,
                    content=editor
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
