import socket
import threading
import time
import network
import json
import server
import client


peers = []
peers_ip = []
network_name_ = ""
password_ = ""


def get_config_data(network_name, password):
    if network_name == "test" and password == "hello123":
        with open("data_from_php.json") as file:
            data = json.load(file)
            return data
    else:
        return None


def connect_to_network(network_name, password, nat_type, external_ip, external_port):
    global peers, network_name_, password_, peers_ip
    network_name_ = network_name
    password_ = password
    config_data = get_config_data(network_name, password)
    if config_data is None:
        print("[ERROR] Invalid network name or password.")
        network_name = input("Enter network name: ")
        password = input("Enter password: ")
        return False
    elif nat_type == "Symmetric NAT" and len(config_data["peers"]) == 0:
        print(
            "[ERROR] Symmetric NAT detected. You will need at least one peer with a NAT type other than Symmetric NAT to establish a connection."
        )
        return False
    else:
        for peer in config_data["peers"]:
            if peer["nat_type"] == "server_no":
                peers_ip.append(peer["ip"])
                continue
            if peer["ip"] == external_ip and peer["port"] == external_port:
                continue
            peers_ip.append(peer["ip"])
            connection_result = client.test_connection(peer["ip"], peer["port"])
            if (not connection_result) and ((peer["ip"], peer["port"]) in peers):
                peers.remove((peer["ip"], peer["port"]))
            else:
                if not (peer["ip"], peer["port"]) in peers:
                    peers.append((peer["ip"], peer["port"]))
        return True


def update_peers(network_name, password, nat_type, external_ip, external_port):
    while True:
        connection_result = connect_to_network(
            network_name, password, nat_type, external_ip, external_port
        )
        if not connection_result:
            print("[DISCONNECTED] Disconnected from the network.")
        time.sleep(5)


def main():
    nat_type, external_ip, external_port = network.get_nat_type()
    print(
        f"NAT Type: {nat_type}, External IP: {external_ip}, External Port: {external_port}"
    )
    if nat_type != "Symmetric NAT":
        threading.Thread(
            target=server.start_server, args=(external_port, peers_ip)
        ).start()
    connection_result = connect_to_network(
        input("Enter network name: "),
        input("Enter password: "),
        nat_type,
        external_ip,
        external_port,
    )
    if not connection_result:
        print("Failed to connect to the network.")
        while True:
            connection_result = connect_to_network(
                input("Enter network name: "),
                input("Enter password: "),
                nat_type,
                external_ip,
                external_port,
            )
            if connection_result:
                break
            time.sleep(5)
    print("Active connections as client: ")
    if len(peers) == 0:
        print("None")
    for i, peer in enumerate(peers):
        print(f"{i}: {peer}")
    threading.Thread(
        target=update_peers,
        args=(
            network_name_,
            password_,
            nat_type,
            external_ip,
            external_port,
        ),
    ).start()
    threading.Thread(target=test_send).start()


def test_send():
    while True:
        for peer_ip in peers_ip:
            message = "Hello from server!"
            server.send_to_client(peer_ip, message)
        time.sleep(5)


if __name__ == "__main__":
    main()
