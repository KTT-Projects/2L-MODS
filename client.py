import socket

HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


def connect_to_server(server):
    client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    try:
        client.connect((server, PORT))
        print("Connected to the server!")
        return True
    except:
        print("[Error:2]")
        return False
