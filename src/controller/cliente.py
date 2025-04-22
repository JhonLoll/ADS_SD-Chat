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

                # Remove a parte da hora da mensagem, e mostra apenas a mensagem em si
                if msg.startswith('[') and ']' in msg:
                    # = [12:34] (Pega apenas a partir daqui): 
                    time_end = msg.index(']') + 1
                    sender_part = msg[time_end:].strip()
                    # = [12:34]: (Pega apenas a partir daqui) 
                    if ': ' in sender_part:
                        sender, message_content = sender_part.split(': ', 1)
                        add_msg(Message(sender.strip(), message_content.strip()))
                    else:
                        add_msg(Message("Sistema", msg))
                else:
                    add_msg(Message("Desconhecido", msg))
            except ConnectionResetError:
                add_msg(Message("Sistema", "Conexão com o servidor perdida"))
            except Exception as e:
                print(f"Erro ao receber mensagem: {e}")
                break
