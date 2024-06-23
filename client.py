import socket
import threading
import time
from config import *

client_sockets = dict()


def receive_from_server(client_socket):
    while True:
        data, addr = client_socket.recvfrom(SIZE)
        if data.decode() == IGNORE_MESSAGE:
            continue
        print(f"[RECEIVED] {data.decode()}")


def send_to_server(server_ip, server_port, data):
    client_sockets[(server_ip, server_port)].send(data.encode())


def test_connection(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.connect((server_ip, server_port))
    client_socket.send(TEST_MESSAGE.encode())
    data, addr = client_socket.recvfrom(SIZE)
    if data.decode() == TEST_MESSAGE:
        client_sockets[(server_ip, server_port)] = client_socket
        receive_thread = threading.Thread(
            target=receive_from_server, args=(client_socket,)
        )
        receive_thread.start()
        print(f"[CONNECTED TO SERVER] {server_ip} : {server_port}")
        return True
    else:
        return False
