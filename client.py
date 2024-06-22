import socket

HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

clients = []
connections = []
message = ""


def connect_to_server(server, port, my_port):
    global clients, connections
    print(f"[CONNECTING TO SERVER] {server} : {port}")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server, port))
        clients.append(client)
        if (server, port, "Failed") in connections:
            connections[connections.index((server, port, "Failed"))] = (
                server,
                port,
                "Connected",
            )
        else:
            connections.append((server, port, "Connected"))
        print(f"[CONNECTED TO SERVER] {server} : {port}")
        print(f"[ACTIVE CONNECTIONS AS CLIENT] {len(clients)}")
        send(str(my_port), client, len(clients) - 1)
        return True
    except:
        connections.append((server, port, "Failed"))
        print("[ERROR] Failed to connect to the server.")
        return False


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
