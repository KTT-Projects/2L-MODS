import socket
import threading
import time
from config import *


def maintain_connection(server_socket, addr):
    while True:
        try:
            data = IGNORE_MESSAGE
            server_socket.sendto(data.encode(), addr)
            time.sleep(0.5)
        except ConnectionResetError:
            print(f"[CONNECTION LOST] Connection lost with {addr}")
            break


def handle_client(server_socket, addr):
    print(f"[NEW CONNECTION] Connected to {addr}")
    connection_thread = threading.Thread(
        target=maintain_connection, args=(server_socket, addr)
    )
    connection_thread.start()
    while True:
        data = server_socket.recv(SIZE)
        if data == DISCONNECT_MESSAGE:
            print(f"[CONNECTION CLOSED] Disconnected from {addr}")
            break
        elif data == IGNORE_MESSAGE:
            continue
        print(f"[{addr}] {data.decode()}")
    server_socket.close()
    print(f"[CONNECTION CLOSED] Disconnected from {addr}")


def start_server(external_port, peers):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("", external_port))
    print("[SERVER STARTED] Waiting for connections...")
    while True:
        data, addr = server_socket.recvfrom(SIZE)
        if addr not in peers:
            print(f"[WARNING] Unauthorized connection from {addr}")
        client_thread = threading.Thread(
            target=handle_client, args=(server_socket, addr)
        )
        client_thread.start()
