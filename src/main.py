import flet as ft
from dotenv import load_dotenv
import os

load_dotenv()

def main(page: ft.Page):
    label = ft.Text("Hello, world!", size=50)

    page.add(
        ft.SafeArea(
            expand=True,                                               content=ft.Container(
                content=label,
                alignment=ft.Alignment.CENTER,
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
