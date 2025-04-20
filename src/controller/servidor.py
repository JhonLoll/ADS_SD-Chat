import socket
import threading
from datetime import datetime

# Lista para armazenar os clientes conectados
clients = []

# Função para o broadcast de mensagens
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                # Envia a mensagem para todos os clientes, exceto o que enviou
                client.send(message)
            except:
                # Se falhar, remove o cliente da lista
                clients.remove(client)

# Função para lidar com cada cliente
def handle_client(client_socket, client_address):
    try:
        nome = client_socket.recv(1024).decode('utf-8')
        print(f"Nome do cliente {client_address}: {nome}")
    except:
        print(f"Erro ao receber o nome do cliente {client_address}.")
        client_socket.close()
        return
    
    boas_vindas = f"[{datetime.now().strftime('%H:%M:%S')}] {nome} entrou no chat!"
    broadcast(boas_vindas, client_socket)

    while True:
        try:
            # Recebe a mensagem do cliente
            msg = client_socket.recv(1024).decode('utf-8')
            if msg:
                horario = datetime.now().strftime('%H:%M:%S')
                broadcast(f"[{horario}] {nome}: {msg}".encode('utf-8'), client_socket)
        except:
            # Se ocorrer um erro, remove o cliente e encerra o loop
            clients.remove(client_socket)
            client_socket.close()
            broadcast(f"[{datetime.now().strftime('%H:%M:%S')}] {nome} saiu do chat.".encode('utf-8'), client_socket)
            break

# Função principal do servidor
def start_server():
    # Cria um socket UDP temporário para pegar o IP de saida
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    # Pega o IP de saida
    host = s.getsockname()[0]

    s.close()

    port = int(input("Digite a porta do servidor: "))
    
    # Cria o socket TCP do servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Associa o socket a um endereço e porta
    server_socket.bind((host, port))

    # Coloca o servidor em modo de escuta
    server_socket.listen(5)

    print(f"Servidor iniciado em {host}:{port}")
    print("Aguardando conexões...")

    while True:
        # Aceita uma nova conexão
        client_socket, client_address = server_socket.accept()
        print(f"Conexão aceita de {client_address}")

        # Adiciona o cliente à lista de clientes conectados
        clients.append(client_socket)

        # Cria uma nova thread para lidar com o cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

        print(f"Atualmente {len(clients)} cliente(s) conectado(s).")

if __name__ == "__main__":
    start_server()