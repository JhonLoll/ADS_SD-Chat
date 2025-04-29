from operator import add
from os import name
import threading
import flet as ft
from datetime import datetime
from controller.cliente import ChatClient
from model.model import ChatMessage, Message
from controller.servidor import broadcast, handle_client

def main(page: ft.Page):
    page.title = "Chat Socket"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.window.width = 400
    page.window.height = 700
    page.scroll = None
    # page.bgcolor = "#D9D9D9"
    page.fonts = {
        "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400&display=swap",
        "RobotoMono": "https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400&display=swap",
    }
    page.theme_mode = ft.ThemeMode.DARK
    # page.theme = ft.Theme(
    #     primary=ft.colors.BLUE_500,
    #     secondary=ft.colors.BLUE_500,
    #     font_family="Roboto",
    #     font_size=14,
    # )

    cliente = ChatClient()

    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )
    name_input = ft.TextField(
        label="Usuário",
        autofocus=True,
    )
    ip_input = ft.TextField(
        label="IP",
        value="127.0.0.1",
    )
    port_input = ft.TextField(
        label="Porta",
        value="5000"
    )
    msg_input = ft.TextField(
        label="Mensagem",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
    )
    send_button = ft.IconButton(
        icon=ft.Icons.SEND_ROUNDED,
        tooltip="Send message",
    )

    login_view = ft.Column(
        controls=[],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    chat_view = ft.Column(
        controls=[
            ft.Container(
                content=chat,
                border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
                border_radius=ft.border_radius.only(top_left=5, top_right=5),
                expand=True,
            ),
            ft.Container(
                ft.Row(
                    controls=[
                        msg_input,
                        send_button
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
            )
            # bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.BLACK),
            # padding=10,
            # border_radius=ft.border_radius.only(top_left=5, top_right=5),
        ],
        expand=True,
        spacing=0,
        visible=False
    )

    def add_msg(msg: Message):
        # Executa o update na thread da UI
        async def update_ui():
            chat.controls.append(
                ChatMessage(message=msg)
            )
            page.update()
        page.run_task(update_ui)

    def send_click(e):
        if msg_input.value:
            # msg = Message(cliente.name, msg_input.value)
            # add_msg(msg)
            cliente.send_message(
                msg_input.value
            )
            msg_input.value = ""
            page.update()
            
    def connect_click(e):
        try:
            cliente.connect(
                ip_input.value,
                int(port_input.value),
                name_input.value
            )
            
            page.snackbar = ft.SnackBar(
                content=ft.Text(
                    f"Conectado como {cliente.name}",
                    bgcolor=ft.Colors.GREEN_500,
                )
            )
            page.snackbar.open = True

            login_view.visible = False
            chat_view.visible = True

            page.update()

            # Trata a exceção com uma thread
            def thread_exception():
                try:
                    cliente.receive_message(add_msg)
                except Exception as e:
                    print(f"Erro na thread: {e}")

            threading.Thread(
                target=thread_exception,
                daemon=True
            ).start()
            
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            page.snackbar = ft.SnackBar(
                ft.Text(
                    f"Erro {str(e)}",
                    color=ft.Colors.RED
                )
            )
            page.snackbar.open = True
            page.update()

    btn_connect = ft.ElevatedButton(
        text="Conectar",
        on_click=connect_click,
        icon=ft.Icons.CONNECT_WITHOUT_CONTACT_ROUNDED,
        bgcolor=ft.Colors.GREEN_500,
        color=ft.Colors.WHITE,
    )
    send_button.on_click = send_click
    msg_input.on_submit = send_click

    login_view.controls.extend(
        [
            name_input,
            ip_input,
            port_input,
            btn_connect
        ]
    )

    page.add(
        ft.Container(
            content=ft.Stack(
                controls=[
                    login_view, chat_view
                ],
                expand=True,
            ),
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets", view=ft.FLET_APP)
