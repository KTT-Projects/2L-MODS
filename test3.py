import socket
import threading
import stun
 
 
def get_nat_type():
    # Determine the NAT type and external IP and port
    nat_type, external_ip, external_port = stun.get_ip_info()
    return nat_type, external_ip, external_port
 
 
def server_mode(server_socket):
    print("Server mode started. Waiting for client...")
    while True:
        data, addr = server_socket.recvfrom(1024)
        print(f"Received message from {addr}: {data.decode()}")
        if data:
            message = input("Enter message: ")
            server_socket.sendto(message.encode(), addr)
 
 
def client_mode(server_ip, server_port, client_socket):
    print("Client mode started. Connecting to server...")
    while True:
        message = input("Enter message: ")
        client_socket.sendto(message.encode(), (server_ip, server_port))
        data, addr = client_socket.recvfrom(1024)
        print(f"Received message from server: {data.decode()}")
 
 
def main():
    nat_type, external_ip, external_port = get_nat_type()
    print(
        f"NAT Type: {nat_type}, External IP: {external_ip}, External Port: {external_port}"
    )
 
    if nat_type == "Symmetric NAT":
        print("Symmetric NAT detected. Only client mode is available.")
        mode = "client"
    else:
        mode = input("Enter mode (server/client): ").strip().lower()
 
    if mode == "server" and nat_type != "Symmetric NAT":
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(("", external_port))
        print(f"Server started on {external_ip}:{external_port}")
        server_thread = threading.Thread(target=server_mode, args=(server_socket,))
        server_thread.start()
        server_thread.join()
    elif mode == "client":
        server_ip = input("Enter server public IP: ").strip()
        server_port = int(input("Enter server public UDP port: ").strip())
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_thread = threading.Thread(
            target=client_mode, args=(server_ip, server_port, client_socket)
        )
        client_thread.start()
        client_thread.join()
    else:
        print(
            "Invalid mode or server mode is not available for symmetric NATs. Exiting."
        )
 
 
if __name__ == "__main__":
    main()
