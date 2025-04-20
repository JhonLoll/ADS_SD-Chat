import socket
import threading
from datetime import datetime

from model.model import Message

class ChatClient:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = ""

    def connect(self, host, port, name):
        self.name = name
        self.socket.connect((host, int(port)))
        self.socket.send(name.encode('utf-8'))

    def send_message(self, message):
        self.socket.send(message.encode('utf-8'))

    def receive_message(self, add_msg):
        while True:
            try:
                msg = self.socket.recv(1024).decode('utf-8')
                if msg:
                    parts = msg.split(": ", 1)
                    if len(parts) == 2:
                        sender, message = parts
                        message = Message(sender.strip(), message.strip(), datetime.now())
                    else:
                        # Mensagens do sistema (entrada, saida, etc..)
                        message = Message("Sistema", msg.strip(), datetime.now())
                    add_msg(message)
            except Exception as e:
                print(f"Erro ao receber mensagem: {e}")
                break
