import socket
import threading
import time
from config import *

clients = []


# def maintain_connection(server_socket, addr):
#     while True:
#         try:
#             data = IGNORE_MESSAGE
#             server_socket.sendto(data.encode(), addr)
#             time.sleep(0.5)
#         except ConnectionResetError:
#             print(f"[CONNECTION LOST] Connection lost with {addr}")
#             break


# def handle_client(server_socket, addr):
#     print(f"[NEW CONNECTION] Connected to {addr}")
#     connection_thread = threading.Thread(
#         target=maintain_connection, args=(server_socket, addr)
#     )
#     connection_thread.start()
#     while True:
#         data = server_socket.recv(SIZE)
#         if data == DISCONNECT_MESSAGE:
#             print(f"[CONNECTION CLOSED] Disconnected from {addr}")
#             break
#         elif data == IGNORE_MESSAGE:
#             continue
#         print(f"[{addr}] {data.decode()}")
#     server_socket.close()
#     print(f"[CONNECTION CLOSED] Disconnected from {addr}")


def send_to_client(server_socket, addr, msg):
    server_socket.sendto(msg.encode(), addr)


def recieve_from_client(server_socket, peers_ip):
    while True:
        data, addr = server_socket.recvfrom(SIZE)
        data = data.decode()
        if addr[0] not in peers_ip:
            print(f"[WARNING] Unauthorized connection from {addr[0]}")
            continue
        if data == TEST_MESSAGE:
            server_socket.sendto(TEST_MESSAGE.encode(), addr)
            clients.append(addr)
            print(f"[NEW CONNECTION] Connected to {addr}")
            continue
        else:
            print(f"[{addr}] {data}")


def start_server(external_port, peers_ip):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("", external_port))
    print("[SERVER STARTED] Waiting for connections...")
    receive_thread = threading.Thread(
        target=recieve_from_client, args=(server_socket, peers_ip)
    )
    receive_thread.start()
