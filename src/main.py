import flet as ft

def main(page: ft.Page):
    def _view_template(
            route: str,
            content
        ):
        return ft.View(
            route=route,
            padding=20,
            controls=[
                ft.SafeArea(
                    expand=True,
                    content=content,
                )
            ]
        )

    def home_view():
        content = ft.Column(
            controls=[
                ft.Text("Hello, world!"),
                ft.Button(
                    "Change",
                    on_click=lambda e: page.navigate("/editor"),
                )
            ]
        )
        return _view_template("/", content)

    def editor_view():
        content = ft.Container(
            expand=True,
            content=ft.TextField(
                expand=True,
                hint_text="Write your ideas here...",
                multiline=True,
                border=ft.NoInputBorder(),
            )
        )
        return _view_template("/editor", content)

    def route_change():
        page.views.clear()
        match page.route:
            case "/":
                page.views.append(home_view())
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
