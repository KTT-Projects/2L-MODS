import socket
import stun
import threading

# List of STUN servers
STUN_SERVERS = [
    ("stun.l.google.com", 19302),
    ("stun1.l.google.com", 19302),
    ("stun2.l.google.com", 19302),
    ("stun3.l.google.com", 19302),
    ("stun4.l.google.com", 19302),
]


def get_public_ip_and_port(stun_host="stun.l.google.com", stun_port=19302):
    nat_type, external_ip, external_port = stun.get_ip_info(
        stun_host=stun_host, stun_port=stun_port
    )
    return nat_type, external_ip, external_port


def collect_stun_mappings():
    mappings = []
    for stun_host, stun_port in STUN_SERVERS:
        nat_type, public_ip, public_port = get_public_ip_and_port(stun_host, stun_port)
        mappings.append((nat_type, public_ip, public_port))
        print(f"STUN Server: {stun_host}:{stun_port}")
        print(f"NAT Type: {nat_type}")
        print(f"Public IP: {public_ip}")
        print(f"Public UDP Port: {public_port}")
        print("-" * 30)
    return mappings


def listen_for_messages(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Message from {addr}: {data.decode()}")


def main():
    print("Collecting STUN mappings...")
    mappings = collect_stun_mappings()

    if mappings:
        nat_type, public_ip, public_port = mappings[0]
        print(f"Your Public IP: {public_ip}")
        print(f"Your Public UDP Port: {public_port}")

        # Create UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("", public_port))

        # Start a thread to listen for incoming messages
        threading.Thread(target=listen_for_messages, args=(sock,), daemon=True).start()

        # Get peer information from user
        peer_ip = input("Enter peer's public IP: ")
        peer_port = int(input("Enter peer's public UDP port: "))

        # Send initial punch-through packet to peer
        sock.sendto(b"Hello from peer", (peer_ip, peer_port))

        print("You can now send messages. Type your message and press Enter.")
        while True:
            message = input()
            sock.sendto(message.encode(), (peer_ip, peer_port))


if __name__ == "__main__":
    main()
