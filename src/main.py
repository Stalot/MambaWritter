import flet as ft
import os
from pathlib import Path

APP_DATA_PATH: Path = Path(os.getenv("FLET_APP_STORAGE_DATA"))
APP_DATA_TEMP_PATH: Path = Path(os.getenv("FLET_APP_STORAGE_TEMP"))
USER_DIR: Path = APP_DATA_PATH / "user"

APP_DATA_PATH.mkdir(parents=True, exist_ok=True)
APP_DATA_TEMP_PATH.mkdir(parents=True, exist_ok=True)
USER_DIR.mkdir(parents=True, exist_ok=True)

async def main(page: ft.Page):
    page.padding = 4
    page.spacing = 2

    def rebuild_current_view(new_view):
        page.views[-1] = new_view
        page.update()
        
    def home_view() -> ft.View:
        async def goto_editor():
            await page.push_route("/editor")
        async def new_file(e):
            page.session.store.set("textbox", "")
            page.session.store.set("title", "")
            page.session.store.set("path", None)
            await goto_editor()
        async def open_file(e):
            file_path: Path = Path(e.control.data)
            with open(file_path, "r") as f:
                content: str = f.read()
            page.session.store.set("path", file_path)
            page.session.store.set("textbox", content)
            page.session.store.set("title", file_path.stem)     
            await goto_editor()

        async def delete_file(e):
            file_path: Path = Path(e.control.data)

            async def proceed(e):
                page.pop_dialog()
                file_path.unlink(missing_ok=True)
                new_view = home_view()
                rebuild_current_view(new_view)

            confirm_delete_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text(
                    "Delete file"
                ),
                content=ft.Text(
                    f"Do you really want to delete '{file_path.name}'?"
                ),
                actions=[
                    ft.TextButton(
                        "Yes",
                        on_click=proceed
                    ),
                    ft.TextButton(
                        "No",
                        on_click=lambda e: page.pop_dialog()
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )

            page.show_dialog(confirm_delete_dialog)


        def user_files():
            path: Path = USER_DIR
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
                    content=ft.ListView(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        expand=True,
                                        alignment=ft.Alignment.CENTER_LEFT,
                                        content=ft.TextButton(
                                                file.name,
                                                data=file.resolve(),
                                                on_click=open_file
                                            ),
                                    ),
                                    ft.Container(
                                        expand=True,
                                        alignment=ft.Alignment.CENTER_RIGHT,
                                        content=ft.IconButton(
                                                ft.Icons.DELETE,
                                                data=file.resolve(),
                                            on_click=delete_file, 
                                            ),
                                    ),
                                ],
                            ) for file in user_files()
                        ]
                    )
                )
            ]
        )
        view.appbar = appBar
        return view

    def editor_view() -> ft.View:
        def default_value(key: str) -> str:
            return page.session.store.get(key)
        async def save_file(e):
            file_title: str = title_field.value

            if not file_title:
                file_title = "Untitled File"

            file_content: str = textbox_field.value
            print(f"{title_field.value=}")
            print(f"{textbox_field.value=}")

            path: Path = USER_DIR / f"{file_title}.txt"
            old_path: Path | None = page.session.store.get("path")
            print(f"{old_path=}")
            with open(path, "w") as f:
                f.write(file_content)

            if old_path != None and old_path.exists():
                os.replace(old_path, path)

        title_field = ft.TextField(
            expand=True,
            border=ft.InputBorder.NONE,
            hint_text="Title",
            value=default_value("title"),
        )

        textbox_field = ft.TextField(
            expand=True,
            border=ft.InputBorder.NONE,
            text_size=16,
            multiline=True,
            hint_text="...",
            value=default_value("textbox"),
        )

        app_bar = ft.AppBar(
            actions=[
                ft.TextButton(
                    "Save",
                    on_click=save_file,
                )
            ]
        )
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
                                    title_field,
                                    #textbox_field,
                                ],
                            ),
                            textbox_field,
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
