import socket                  # Importa o módulo de rede
from threading import Thread   # Importa suporte para execução em threads (paralelismo)

client_list = []               # Lista para armazenar todos os clientes conectados

# Função que lida com a comunicação com cada cliente
def Chat(client_socket):
    while True:
        try:
            # Recebe a mensagem do cliente
            mensagem = client_socket.recv(1024).decode()
            if not mensagem or mensagem == "sair":  # Se for vazio ou sair, encerra a conexão
                break

            # Envia a mensagem para todos os outros clientes conectados
            for client in client_list:
                if client != client_socket:
                    client.send(mensagem.encode())

        except Exception as e:
            # Exibe erro se houver problema ao receber/enviar
            print(f"Erro: {e}")
            break

    # Remove o cliente da lista e fecha o socket ao sair
    client_list.remove(client_socket)
    client_socket.close()

# Captura o IP local da máquina de forma confiável
# Isso funciona mesmo que a máquina tenha vários IPs (ex: Wi-Fi, Ethernet)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Cria um socket UDP temporário
s.connect(("8.8.8.8", 80))                            # Conecta ao DNS do Google
host = s.getsockname()[0]                             # Pega o IP local usado para "sair" para a internet
s.close()                                             # Fecha o socket temporário

port = 12345  # Porta em que o servidor irá escutar

# Cria o socket TCP para o servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa o socket ao IP e porta definidos
server_socket.bind((host, port))

# Informa no terminal onde o servidor está rodando
print(f"Servidor iniciado em {host}:{port}")

# Coloca o socket em modo de escuta (aguardando conexões), até 5 pendências
server_socket.listen(5)

print("Aguardando conexões...")

# Loop infinito para aceitar várias conexões
while True:
    # Aceita uma nova conexão
    client_socket, client_address = server_socket.accept()
    print(f"Conexão estabelecida com {client_address}")  # Exibe IP/porta do cliente

    # Adiciona o cliente à lista
    client_list.append(client_socket)

    # Cria e inicia uma nova thread para lidar com o cliente
    Thread(target=Chat, args=(client_socket,)).start()
