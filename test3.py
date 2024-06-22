import requests
import socket
import threading
import time
 
# Server URL
php_server_url = "https://kttprojects.com/tcp_port.php"
 
# Unique identifier for this client (make sure to change this for the second client)
client_id = "client2"  # Change to 'client2' for the other client
 
 
# Function to register the client with the PHP server
def register_client(port):
    data = {"client_id": client_id, "port": port}
    response = requests.post(php_server_url, data=data)
    print(f"Register response: {response.text}")
 
 
# Function to retrieve another client's information
def get_client_info(other_client_id):
    response = requests.get(php_server_url, params={"client_id": other_client_id})
    return response.json()
 
 
# Function to handle UDP hole punching
def udp_hole_punch(local_port, remote_ip, remote_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", local_port))
    print(f"Listening on UDP port {local_port}")
 
    def listen():
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                print(f"Received message: {data.decode()} from {addr}")
            except Exception as e:
                print(f"Listening error: {e}")
                break
 
    listening_thread = threading.Thread(target=listen, daemon=True)
    listening_thread.start()
 
    # Send a message to the remote client to create the mapping
    for _ in range(10):  # Send multiple times to ensure the mapping is created
        sock.sendto(b"Hello", (remote_ip, remote_port))
        print(f"Sent message to {remote_ip}:{remote_port}")
        time.sleep(1)  # Send every 1 second
 
    listening_thread.join()
 
 
# Main function
def main():
    local_udp_port = 54321  # Local UDP port to listen on
 
    # Register this client with the PHP server
    register_client(local_udp_port)
 
    # Ensure the other client has also registered before attempting to get their info
    other_client_id = "client2" if client_id == "client1" else "client1"
 
    other_client_info = {}
    while "error" in other_client_info or not other_client_info:
        other_client_info = get_client_info(other_client_id)
        if "error" in other_client_info:
            print(f"Error: {other_client_info['error']}. Retrying...")
            time.sleep(5)  # Wait for 5 seconds before retrying
        else:
            print(f"Retrieved client info: {other_client_info}")
 
    remote_ip = other_client_info.get("ip")
    remote_port = int(other_client_info.get("port"))
 
    # Perform UDP hole punching
    udp_hole_punch(local_udp_port, remote_ip, remote_port)
 
    # Keep the script running indefinitely
    while True:
        time.sleep(1)
 
 
if __name__ == "__main__":
    main()
 