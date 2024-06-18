# Error codes
# 1: No internet connection


# Libraries
# socket -> internet connection
# threading -> multiple connections (concurrent execution)
# requests -> getting public IP
# urllib -> checking internet connection
# ip_address -> checking IP version


HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


import socket
import threading
from requests import get
import urllib.request
from ipaddress import ip_address


def check_internet_connection():
    try:
        urllib.request.urlopen("https://www.google.com")
        return True
    except urllib.error.URLError:
        return False


def get_public_ip():
    if check_internet_connection():
        return get("https://api64.ipify.org").text
    else:
        return "[Error:1]"


def is_ipv4(ip):
    if ip_address(ip).version == 4:
        return True
    else:
        return False


def is_ipv6(ip):
    if ip_address(ip).version == 6:
        return True
    else:
        return False


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
    if check_internet_connection():
        SERVER = get_public_ip()
        ADDR = (SERVER, PORT)
        if is_ipv4(SERVER):
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif is_ipv6(SERVER):
            server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        server.bind(ADDR)
        server.listen()
        print(f"Listening on {SERVER}")
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
