import socket
import threading
import time
from config import *

server_socket = None
addrs = dict()
clients = []
peers_ip_ = []


def send_to_client(client_ip, msg):
    global server_socket, addrs
    if addrs.get(client_ip) is not None:
        server_socket.sendto(msg.encode(), addrs[client_ip])


def recieve_from_client():
    global clients, addrs, server_socket, peers_ip_
    while True:
        data, addr = server_socket.recvfrom(SIZE)
        data = data.decode()
        if addr[0] not in peers_ip_:
            print(f"[WARNING] Unauthorized connection from {addr[0]}")
            continue
        if data == TEST_MESSAGE:
            server_socket.sendto(TEST_MESSAGE.encode(), addr)
            clients.append(addr)
            addrs[addr[0]] = addr
            print(f"[NEW CONNECTION] Connected to {addr}")
            continue
        else:
            print(f"[{addr}] {data}")


def start_server(external_port):
    global server_socket, peers_ip_
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("", external_port))
    print("[SERVER STARTED] Waiting for connections...")
    receive_thread = threading.Thread(
        target=recieve_from_client,
    )
    receive_thread.start()
