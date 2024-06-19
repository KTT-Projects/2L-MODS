import socket
import network
import threading

HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

clients = []
connections = []
message = ""


def connect_to_server(server, port):
    global clients, connections
    print(f"Connecting to {server} : {port}")
    if network.is_ipv4(server):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    elif network.is_ipv6(server):
        client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    try:
        client.connect((server, port))
        clients.append(client)
        connections.append((server, port, "Connected"))
        print(f"[CONNECTED TO SERVER] {server} : {port}")
        print(f"[ACTIVE CONNECTIONS AS CLIENT] {len(clients)}")
        send(str(port), client, len(clients) - 1)
    except:
        connections.append((server, port, "Failed"))
        print("[Error:2]")
        return


def send(msg, client, index):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(f"[SENT] {msg}")
    if msg == DISCONNECT_MESSAGE:
        client.shutdown(socket.SHUT_RDWR)
        client.close()
        print("Disconnected from the server.")
        clients.remove(client)
        connections.remove((connections[index][0], connections[index][1], "Connected"))
        return
