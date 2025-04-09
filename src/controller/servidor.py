import threading, socket, socketserver

def server(host, port, handler):
    """Starts a server that listens for incoming connections."""
    server = socketserver.TCPServer((host, port), handler)
    server.serve_forever()

server('localhost', 9999, socketserver.StreamRequestHandler)