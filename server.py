import socket
import threading
from requests import get
from ipaddress import ip_address


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


def start_server(external_ip, external_port):
    global port
    global server_address
    global is_listening
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = (external_ip, external_port)
    try:
        server.bind(addr)
    except OSError:
        print(f"[ERROR] Port {external_port} is already in use.")
        return
    port = external_port
    server_address = external_ip
    server.listen()
    is_listening = True
    print(f"Listening on {server_address} : {port}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
