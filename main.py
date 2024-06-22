import socket
import threading
import network
import json
import server

# def server_mode(server_socket):
#     print("Server mode started. Waiting for client...")
#     while True:
#         data, addr = server_socket.recvfrom(1024)
#         print(f"Received message from {addr}: {data.decode()}")
#         if data:
#             message = input("Enter message: ")
#             server_socket.sendto(message.encode(), addr)


# def client_mode(server_ip, server_port, client_socket):
#     print("Client mode started. Connecting to server...")
#     while True:
#         message = input("Enter message: ")
#         client_socket.sendto(message.encode(), (server_ip, server_port))
#         data, addr = client_socket.recvfrom(1024)
#         print(f"Received message from server: {data.decode()}")


# def main():
#     nat_type, external_ip, external_port = network.get_nat_type()
#     print(
#         f"NAT Type: {nat_type}, External IP: {external_ip}, External Port: {external_port}"
#     )

#     if nat_type == "Symmetric NAT":
#         print("Symmetric NAT detected. Only client mode is available.")
#         mode = "client"
#     else:
#         mode = input("Enter mode (server/client): ").strip().lower()

#     if mode == "server" and nat_type != "Symmetric NAT":
#         server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         server_socket.bind(("", external_port))
#         print(f"Server started on {external_ip}:{external_port}")
#         server_thread = threading.Thread(target=server_mode, args=(server_socket,))
#         server_thread.start()
#         server_thread.join()
#     elif mode == "client":
#         server_ip = input("Enter server public IP: ").strip()
#         server_port = int(input("Enter server public UDP port: ").strip())
#         client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         client_thread = threading.Thread(
#             target=client_mode, args=(server_ip, server_port, client_socket)
#         )
#         client_thread.start()
#         client_thread.join()
#     else:
#         print(
#             "Invalid mode or server mode is not available for symmetric NATs. Exiting."
#         )


def get_config_data(network_name, password):
    if network_name == "test" and password == "hello123":
        with open("data_from_php.json") as file:
            data = json.load(file)
            return data
    else:
        return None


def connect_to_network(network_name, password, nat_type):
    print(f"Connecting to {network_name}")
    config_data = get_config_data(network_name, password)
    if config_data is None:
        print("Invalid network name or password.")
        network_name = input("Enter network name: ")
        password = input("Enter password: ")
        return connect_to_network(network_name, password, nat_type)
    elif nat_type == "Symmetric NAT" and len(config_data["peers"]) == 0:
        print(
            "[ERROR] Symmetric NAT detected. You will need at least one peer with a NAT type other than Symmetric NAT to establish a connection."
        )
        return False
    else:
        print("Connection established.")
        for peer in config_data["peers"]:
            client_socket = connect_to_server(peer["ip"], peer["port"])
            send_message(client_socket, "Hello from client!")
        return True


def main():
    nat_type, external_ip, external_port = network.get_nat_type()
    print(
        f"NAT Type: {nat_type}, External IP: {external_ip}, External Port: {external_port}"
    )
    if nat_type != "Symmetric NAT":
        server.start_server(external_ip, external_port)
    connection_result = connect_to_network(
        input("Enter network name: "), input("Enter password: "), nat_type
    )


if __name__ == "__main__":
    main()
