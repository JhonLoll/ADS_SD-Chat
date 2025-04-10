import flet as ft

from model.model import Message, ChatMessage

def main(page: ft.Page):
    page.title = "Chat Socket"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20

    def join_chat(e):
        if not user_name.value:
            user_name.error_text = "Por favor, insira seu nome."
            user_name.update()
        else:
            page.session.set("user_name", user_name.value)
            set_user_name.open = False
            message_input.prefix = ft.Text(f"{user_name.value}: ")
            page.pubsub.send_all(
                Message(
                    sender=user_name.value, 
                    content="Entrou no chat", 
                    message_type="system"
                )
            )
            page.update()

    def send_message(content: str, user_name: str = "User"):
        if content:
            message = Message(sender=user_name, content=content)
            message_list.controls.append(ChatMessage(message))
            message_input.value = ""  # Limpa o campo de input
            message_input.focus()  # Retorna o foco para o campo de input
            page.update()

    def on_message(message: Message):
        message_list.controls.append(ChatMessage(message))
        page.update()

    page.pubsub.subscribe(
        on_message
    )

    user_name = ft.TextField(
        label="Digite seu nome", 
        width=400, 
        on_submit=lambda e: join_chat
    )

    set_user_name = ft.AlertDialog(
        title=ft.Text("Bem-vindo ao Chat", size=20),
        content=ft.Column(
            [
                user_name,
                ft.TextButton(
                    text="Entrar",
                    on_click=lambda e: join_chat,
                ),
            ],
            spacing=10,
        ),
    )

    # Linha do campo de input
    message_input = ft.TextField(
        label="Digite sua mensagem",
        expand=True,
        on_submit=lambda e: send_message(e.control.value, user_name.value),
    )    
    input_row = ft.Row(
        controls=[
            message_input,
            ft.IconButton(
                icon=ft.Icons.SEND,
                tooltip="Enviar",
                on_click=lambda e: send_message(message_input.value, user_name.value),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    
    # Adiciona o campo de mensagens
    message_list = ft.ListView(
        spacing=10,
        expand=True,  # Faz com que o ListView ocupe o espaço disponível
    )

    # Adiciona os controles à página
    page.add(
        ft.Column(
            [
                message_list,
                input_row,
            ],
            expand=True,
            spacing=10,
        )
    )

    # Exibe o diálogo de configuração do nome de usuário
    set_user_name.open = True
    page.overlay.append(set_user_name)

    page.update()

ft.app(target=main)