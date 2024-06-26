import socket
import threading
import time
from config import *

clients = []


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
