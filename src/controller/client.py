import threading, client, socket, socketserver

def client(host, port):
    """Starts a client that connects to a server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        # Client logic here
        # For example, send a message to the server
        s.sendall(b'Hello, server!')

        data = s.recv(1024)

        print('Received', repr(data))

client('localhost', 9999)