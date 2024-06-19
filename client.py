import socket
import network
import time

HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

clients = []
connections = []


def connect_to_server(server, port):
    print(f"Connecting to {server} : {port}")
    if network.is_ipv4(server):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    elif network.is_ipv6(server):
        client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    try:
        client.connect((server, port))
        clients.append(client)
        connections.append((server, port, "Connected"))
        print("Connected to the server!")
        send("Hello World!", client)
        while True:
            send("Hello World!", client)
            time.sleep(10)  # execute every 10 seconds
    except:
        connections.append((server, port, "Failed"))
        print("[Error:2]")
        return


def send(msg, client):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
