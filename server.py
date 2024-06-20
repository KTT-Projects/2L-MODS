import socket
import threading
from requests import get
from ipaddress import ip_address
import network


HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
port = -1
server_address = ""
is_listening = False
connections = dict()


def handle_client(conn, addr):
    global connections
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if not msg_length:
                break
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if connections.get(addr) is None:
                connections[addr] = msg
                print(f"[NEW CONNECTION] {addr[0]} : {msg} connected.")
                print(f"[ACTIVE CONNECTIONS AS SERVER] {len(connections)}")
            elif msg == DISCONNECT_MESSAGE:
                connected = False
            else:
                print(f"[{addr[0]} : {connections[addr]}] {msg}")
        except ConnectionResetError:
            connected = False
    conn.close()
    connections.pop(addr)
    print(f"[DISCONNECTED] {addr[0]} : {connections[addr]} disconnected.")
    print(f"[ACTIVE CONNECTIONS AS SERVER] {len(connections)}")


def start_server():
    global port
    global server_address
    global is_listening
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
                print("[ERROR] No available ports.")
                return
            addr = (server_address, port)
            try:
                server.bind(addr)
                break
            except OSError:
                print(f"Port {port} is occupied. Trying another port...")
            port += 1
        server.listen()
        is_listening = True
        print(f"Listening on {server_address} : {port}")
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
    else:
        print("[ERROR] No internet connection.")
