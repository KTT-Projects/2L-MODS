import socket
import threading
import time
from config import *


def maintain_connection(server_socket, addr):
    while True:
        try:
            data = IGNORE_MESSAGE
            data_length = str(len(data)).encode(FORMAT)
            server_socket.sendto(data_length.encode(FORMAT), addr)
            server_socket.sendto(data.encode(FORMAT), addr)
            time.sleep(5)
        except ConnectionResetError:
            print(f"[CONNECTION LOST] Connection to {addr} lost.")
            break


def handle_client(server_socket, addr):
    print(f"[NEW CONNECTION] Connected to {addr}")
    connection_thread = threading.Thread(
        target=maintain_connection, args=(server_socket, addr)
    )
    connection_thread.start()
    while True:
        data_length = server_socket.recv(HEADER).decode(FORMAT)
        data_length = int(data_length)
        data = server_socket.recv(data_length).decode(FORMAT)
        if data == DISCONNECT_MESSAGE:
            print(f"[CONNECTION CLOSED] Disconnected from {addr}")
            break
        elif data == IGNORE_MESSAGE:
            continue
        print(f"[{addr}] {data}")
    server_socket.close()
    print(f"[CONNECTION CLOSED] Disconnected from {addr}")


def start_server(external_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("", external_port))
    print("[SERVER STARTED] Waiting for connections...")
    while True:
        data, addr = server_socket.recvfrom(HEADER)
        client_thread = threading.Thread(
            target=handle_client, args=(server_socket, addr)
        )
        client_thread.start()
