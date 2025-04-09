import flet as ft
from model.model import Message, ChatMessage

class UserNameView(ft.AlertDialog):
    def __init__(self, page: ft.Page, on_submit: callable):
        super().__init__()
        self.page = page
        self.on_submit = on_submit

        self.title = "Qual o seu nome?"
        self.content = ft.Column([
            ft.TextField(label="Nome", autofocus=True),
            ft.Row([
                ft.ElevatedButton("Confirmar", on_click=self.submit_name),
                ft.ElevatedButton("Cancelar", on_click=self.cancel)
            ])
        ], spacing=10)

    def submit_name(self, e):
        name = self.content.controls[0].value.strip()
        if name:
            self.on_submit(name)
            self.page.dialog = None
            self.page.update()

    def cancel(self, e):
        self.page.dialog = None
        self.page.update()
