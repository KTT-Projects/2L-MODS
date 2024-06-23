# 2L-MODS

2L-MODS is a Python program that enables users to build and manage peer-to-peer (P2P) networks easily. It allows peers to connect, communicate, and maintain connections within a network.

## Features

- Establishes P2P connections using NAT traversal techniques.
- Maintains a list of peers and their IP addresses.
- Handles dynamic peer updates to keep the network connected.
- Provides basic client-server messaging capabilities.

## Prerequisites

- Python 3.x
- Required Python packages: `socket`, `threading`, `time`, `json`
- External packages: `requests`, `pystun3`

## Getting Started

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/KTT-Projects/2L-MODS.git
   cd 2l-MODS
   ```

2. Install the necessary Python packages:
   ```bash
   pip install requests pystun3
   ```

### Configuration

Ensure you have a `data_from_php.json` file in the same directory with the following structure:

```json
{
  "network_name": "test",
  "peers": [
    {
      "ip": "Your Public IP Here",
      "port": Your Public UDP Port Here,
      "nat_type": "server_ok"
    },
    {
      "ip": "Your Public IP Here",
      "port": Your Public UDP Port Here,
      "nat_type": "server_no" (When Symmetric NAT is in use)
    }
  ],
  "model_distributor": {
    "ip": "Your Public IP Here",
    "port": Your Public UDP Port Here
  }
}
```

### Running the Program

To start the program, run:

```bash
python main.py
```

### Usage

1. Enter the network name and password when prompted.
2. The program will determine the NAT type, external IP, and port.
3. If the NAT type is not "Symmetric NAT", the program will start a server thread to listen for incoming connections.
4. The program will attempt to connect to the network using the provided credentials.
5. The program will display active connections as a client and periodically update the peer list.

## File Structure

- `main.py`: The main script to start the P2P network builder.
- `network.py`: Contains the function `get_nat_type()` to get the NAT type, external IP, and port.
- `server.py`: Contains the server implementation to handle incoming client connections.
- `client.py`: Contains the client implementation to handle outgoing server connections.
- `config.py`: Configuration constants such as `SIZE`, `TEST_MESSAGE`, `IGNORE_MESSAGE`.
- `data_from_php.json`: Contains the network configuration data.

## Functions

### Main Functions

- `get_config_data(network_name, password)`: Retrieves network configuration data from `data_from_php.json`.
- `connect_to_network(network_name, password, nat_type, external_ip, external_port)`: Connects to the P2P network.
- `update_peers(network_name, password, nat_type, external_ip, external_port)`: Periodically updates the peer list.
- `main()`: The main function to start the program.

### Server Functions

- `send_to_client(server_socket, addr, msg)`: Sends a message to a client.
- `recieve_from_client(server_socket, peers_ip)`: Receives messages from clients.
- `start_server(external_port, peers_ip)`: Starts the server to listen for client connections.

### Client Functions

- `receive_from_server(client_socket)`: Receives messages from the server.
- `send_to_server(server_ip, server_port, data)`: Sends a message to the server.
- `test_connection(server_ip, server_port)`: Tests the connection to a server.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For questions or support, please contact [info@kttprojects.com](mailto:info@kttprojects.com).
