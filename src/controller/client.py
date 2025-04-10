import socket
import flet as ft

def client(host: str, port: int):
    # Cria o socket do cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conecta ao servidor
    client_socket.connect((host, port))

    # Informa que o cliente foi conectado ao servidor
    print(f"Conectado ao servidor {host}:{port}")

    msg = ""

    while msg != "sair":
        # Lê a mensagem do usuário
        msg = input("Digite sua mensagem (ou 'sair' para encerrar): ")
        # Envia a mensagem para o servidor
        client_socket.send(msg.encode())
        # Recebe a resposta do servidor
        resposta = client_socket.recv(1024).decode()
        # Exibe a resposta do servidor
        print(f"Servidor: {resposta}")

    # Fecha o socket do cliente
    client_socket.close()
    print("Conexão encerrada.")

# Exemplo de uso
if __name__ == "__main__":
    # Captura automaticamente o IP do servidor
    host = socket.gethostbyname(socket.gethostname())
    port = 12345

    client(host, port)



    