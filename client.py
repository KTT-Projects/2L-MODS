import socket

HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


def connect_to_server(server, port):
    print(f"Connecting to {server} : {port}")
    client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    try:
        client.connect((server, int(port)))
        print("Connected to the server!")
        return True
    except:
        print("[Error:2]")
        return False
