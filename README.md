# 2L-MODS (Large Language Model on Distributed Systems)

2L-MODS is a pure P2P distributed system that allows you to run large language models which are too big to fit on a single machine. It is designed to be simple, efficient, and easy to use.

## Installation

### Dependencies

- Python (tested in version 3.10.3 or higher)
- Requests (tested in version 2.31.0 or higher)

To install Python, visit the official Python website and follow the instructions for your operating system.

To install Requests, use the following command:

```sh
pip install requests
```

### Usage

Once you have installed the dependencies, you can run the system by executing the following command:

```sh
python main.py
```

### Configuration

Edit the config.json file to change the configuration of the system. You'll need to manually set up the IP addresses of the nodes in the system. When you run the system for the first time, you'll need to set the "distribute" flag to "true" in the config.json file to distribute the model across the nodes. Set the "model_distributor" to the IP address and the port of the node that will distribute the model. When all the nodes already have the model, you can set the "distribute" flag to "false" to run the model.

If you want to start a new network, backup the content of the "data" folder and delete the content inside it.

### Files

- main.py: The main entry point of the application.
- network.py: Contains network-related functions.
- server.py: Handles server-side operations.
- client.py: Handles client-side operations.
- config.json: Configuration file for the system.
- data/: Folder for storing data.

### License

This project is licensed under the MIT License. See the LICENSE.md file for details.
