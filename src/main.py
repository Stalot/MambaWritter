import flet as ft

def main(page: ft.Page):
    page.padding = 0
    page.spacing = 0
    
    text_field = ft.TextField(
        expand=True,
        border=ft.InputBorder.NONE,
        hint_text="Type here...",
        text_size=16,
        multiline=True,
    )
    top_bar = ft.Row(
            tight=True,
            controls=[
                ft.Container(
                    ft.Row(
                        controls=[
                            ft.Text("MambaWritter")
                            ]
                        )
                    )
                ]
            )
    main_container = ft.Container(
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                top_bar,
                text_field
            ],
        ),
    )
    page.add(ft.SafeArea(
                expand=True,
                content=main_container,
            )
    )

ft.run(main)
