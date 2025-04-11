from http import client
import flet as ft
import socket
from threading import Thread
# from controller.servidor import Chat, client_list
from model.model import Message, ChatMessage

# Variável global para o socket do cliente
client_socket = None

def main(page: ft.Page):
    page.title = "Chat Socket"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.padding = 20

    # Função para conectar ao servidor
    def connect_to_server(host: str, port: int):
        # Permite alterar a variável global client_socket
        global client_socket
        try:
            # Cria o socket do cliente
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Conecta ao servidor
            client_socket.connect((host, port))
            page.client_socket = client_socket  # Armazena o socket do cliente na página
            print(f"Conectado ao servidor {host}:{port}")

            # Inicia uma thread para receber mensagens do servidor
            Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

        except Exception as e:
            print(f"Erro ao conectar ao servidor: {e}")
            page.snackbar = ft.Snackbar(
                content=ft.Text(f"Erro ao conectar ao servidor: {e}"),
                open=True,
            )
            page.update()

    # Função para receber mensagens do servidor
    def receive_messages(client_socket):
        while True:
            try:
                # Recebe a mensagem do servidor
                mensagem = client_socket.recv(1024).decode()
                if not mensagem:
                    break

                # Adiciona a mensagem à lista de mensagens
                message = Message(sender="Servidor", content=mensagem)
                message_list.controls.append(ChatMessage(message))
                page.update()

            except Exception as e:
                print(f"Erro ao receber mensagem: {e}")
                break

        client_socket.close()
        print("Conexão encerrada.")


    # Função que exibe a mensagem quando o usuário entrar no chat
    def join_chat(e):
        if not user_name.value:
            user_name.error_text = "Por favor, insira seu nome."
            user_name.update()
        else:
            page.session.set("user_name", user_name.value)
            set_user_name.open = False
            message_input.prefix = ft.Text(f"{user_name.value}: ")
            # Envia a mensagem de "entrou no chat" para todos os usuarios
            client_socket.send(
                f"{user_name.value} entrou no chat".encode()
            )
            # Conecta ao servidor com o host e porta informados
            connect_to_server(host_input.value, int(port_input.value))
            # Esconde o diálogo de configuração do nome de usuário
            user_name.visible = False,
            page.update()

    # Função que exibe a mensagem quando o usuário sair do chat
    def leave_chat(e):
        # Envia a mensagem de "saiu do chat" para todos os usuarios
        if client_socket:
            client_socket.send(
                f"{user_name.value} saiu do chat".encode()
            )
            client_socket.close()
        # Limpa a lista de mensagens
        page.pubsub.unsubscribe(
            on_message
        )
        page.session.clear()
        page.update()

    # Função que envia a mensagem para o chat
    def send_message(content: str, user_name: str = "User"):
        if content:
            try:
                # Envia a mensagem para o servidor
                client_socket.send(
                    f"{user_name.value}: {content}".encode()
                )
            except Exception as e:
                print(f"Erro ao enviar mensagem: {e}")
                page.snackbar = ft.Snackbar(
                    content=ft.Text(f"Erro ao enviar mensagem: {e}"),
                    open=True,
                )
                page.update()
            # Cria a mensagem com o nome do usuário
            message = Message(sender=user_name, content=content)
            # Adiciona a mensagem à lista de mensagens
            message_list.controls.append(ChatMessage(message))
            message_input.value = ""  # Limpa o campo de input
            message_input.focus()  # Retorna o foco para o campo de input
            page.update()

    # Função que exibe a mensagem quando o usuário enviar uma mensagem
    def on_message(message: Message):
        message_list.controls.append(ChatMessage(message))
        page.update()

    # Subscreve na sessão para receber mensagens
    page.pubsub.subscribe(
        on_message
    )

    # Adiciona o evento de fechar a página
    page.on_close = leave_chat

    # Cria o campo de input para o host
    host_input = ft.TextField(
        label="Host", 
        width=400, 
        hint_text=socket.gethostbyname(socket.gethostname())
    )
    # Cria o campo de input para a porta
    port_input = ft.TextField(
        label="Porta", 
        width=400, 
        hint_text="12345"
    )
    # Cria o campo de input para o nome de usuário
    user_name = ft.TextField(
        label="Digite seu nome", 
        width=400,
    )

    # Cria o diálogo de configuração do nome de usuário
    set_user_name = ft.AlertDialog(
        title=ft.Text("Bem-vindo ao Chat", size=20),
        content=ft.Column(
            [
                host_input,
                port_input,
                user_name,
                ft.TextButton(
                    text="Entrar",
                    on_click=lambda e: join_chat(e),
                ),
            ],
            expand=False,
            alignment=ft.MainAxisAlignment.CENTER,
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
        auto_scroll=True,  # Permite rolagem automática
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

    # Adiciona o EventDialog ao overlay da página
    page.overlay.append(
        set_user_name
    )

    page.update()

ft.app(target=main)