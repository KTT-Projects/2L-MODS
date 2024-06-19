# Error codes
# 1: No internet connection
# 2: Connection error
# 3: All ports occupied


# Libraries
# socket -> internet connection
# threading -> multiple connections (concurrent execution)
# requests -> getting public IP
# urllib -> checking internet connection
# ip_address -> checking IP version


# Header -> length of the message in bytes
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
port = -1
server_address = ""  # public IP


import socket
import threading
from requests import get
from ipaddress import ip_address
import network


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            connected = False
        print(f"[{addr}] {msg}")
    conn.close()


def start_server():
    global port
    global server_address
    if network.check_internet_connection():
        server_address = network.get_public_ip()
        if network.is_ipv4(server_address):
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif network.is_ipv6(server_address):
            server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        while True:
            if port == -1:
                port = 5050
            if port > 65535:
                print("[Error:3]")
                return False
            addr = (server_address, port)
            try:
                server.bind(addr)
                break
            except OSError:
                print(f"Port {port} is occupied. Trying another port...")
            port += 1
        server.listen()
        print(f"Listening on {server_address} : {port}")
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
    else:
        print("[Error:1]")
