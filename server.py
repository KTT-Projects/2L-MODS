import socket
import threading
import time
from config import *

server_sockets = dict()
addrs = dict()
clients = []


def send_to_client(client_ip, msg):
    server_sockets[client_ip].sendto(msg.encode(), addrs[client_ip])


def recieve_from_client(server_socket, peers_ip):
    global clients, server_sockets, addrs
    while True:
        data, addr = server_socket.recvfrom(SIZE)
        data = data.decode()
        if addr[0] not in peers_ip:
            print(f"[WARNING] Unauthorized connection from {addr[0]}")
            continue
        if data == TEST_MESSAGE:
            server_socket.sendto(TEST_MESSAGE.encode(), addr)
            clients.append(addr)
            server_sockets[addr] = server_socket
            addrs[addr[0]] = addr
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
