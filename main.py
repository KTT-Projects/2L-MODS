import os
from tkinter import *
from tkinter import messagebox
import server
import client
import threading
import json


def start_server_thread():
    server.start_server()


def start_client_thread(server_address, port_number):
    client.connect_to_server(server_address, port_number, server.port)


def connect_to_server(server_address, port_number):
    if (server_address, port_number, "Connected") in client.connections:
        return
    # Prevent the user from connecting to their own server
    if server_address == server.server_address and port_number == server.port:
        messagebox.showerror(
            "Connection Error",
            "⚠️ Self-Connection\n\nYou cannot connect to your own server.",
        )
        return
    # Start a new client connection in a separate thread
    client_thread = threading.Thread(
        target=start_client_thread,
        args=(
            server_address,
            port_number,
        ),
    )
    client_thread.start()
    # Check the connection status periodically
    root.after(100, check_connection_status, server_address, port_number)


def check_connection_status(server_address, port_number):
    if (server_address, port_number, "Connected") in client.connections:
        current_text = connection_status_label.cget("text")
        if current_text == "Status: 🔴 Disconnected":
            current_text = ""
        new_text = f"{current_text}[{client.connections.index((server_address, port_number, 'Connected'))}] Status: 🟢 Connected to {server_address} : {port_number}\n"
        connection_status_label.config(text=new_text)
    elif (server_address, port_number, "Failed") in client.connections:
        current_text = connection_status_label.cget("text")
        if (
            f"Status: ⚠️ Connection Failed to {server_address} : {port_number}"
            in current_text
        ):
            return
        if current_text == "Status: 🔴 Disconnected":
            current_text = ""
        new_text = f"{current_text}[{client.connections.index((server_address, port_number, 'Failed'))}] Status: ⚠️ Connection Failed to {server_address} : {port_number}\n"
        connection_status_label.config(text=new_text)
        # client.connections.remove((server_address, port_number, "Failed"))
    else:
        root.after(100, check_connection_status, server_address, port_number)


def observe_server_port_change():
    # Check for changes in the server.port variable
    if server.is_listening:
        user_status.config(
            text=f"Listening on {server.server_address} : {server.port}\n"
        )
        return
    # Schedule the next observation
    root.after(100, observe_server_port_change)


def send_message():
    if not client.connections:
        messagebox.showerror(
            "Connection Error",
            "⚠️ No Connections\n\nPlease connect to a server before sending a message.",
        )
        return
    elif not id_entry.get() or not int(id_entry.get()) < len(client.clients):
        messagebox.showerror(
            "ID Error",
            "⚠️ No ID\n\nPlease enter a correct ID of the server you want to send a message to.",
        )
        return
    elif not message_entry.get():
        messagebox.showerror(
            "Message Error",
            "⚠️ No Message\n\nPlease enter a message to send.",
        )
        return
    selected_id = id_entry.get()
    message = message_entry.get()
    # Send the message to the selected ID
    client.send(message, client.clients[int(selected_id)], int(selected_id))
    message_entry.delete(0, END)
    if message == client.DISCONNECT_MESSAGE:
        id_entry.delete(0, END)
        update_all_connections()


def update_all_connections():
    # Reset the connections list once and update it
    connection_status_label.config(text="")
    if len(client.connections) == 0:
        connection_status_label.config(text="Status: 🔴 Disconnected")
        return
    new_text = ""
    for connection in client.connections:
        new_text += f"[{client.connections.index(connection)}] Status: 🟢 Connected to {connection[0]} : {connection[1]}\n"
    connection_status_label.config(text=new_text)


def load_config():
    global config_data
    try:
        with open("config.json", "r") as file:
            config_data = json.load(file)
        return True
    except FileNotFoundError:
        print("[ERROR] Config file not found.")
        messagebox.showerror(
            "Config Error",
            "⚠️ Config File Not Found\n\nPlease create a config.json file.",
        )
        return False


def attempt_connection():
    for peer in config_data["peers"]:
        if peer["ip"] != server.server_address or peer["port"] != server.port:
            print(f"[INFO] Connecting to {peer['ip']} : {peer['port']}")
            connect_to_server(peer["ip"], peer["port"])


def data_setup():
    # Create a folder for the data if it doesn't exist
    try:
        os.mkdir("./data/" + config_data["network_name"])
    except FileExistsError:
        pass


def join_network():
    print("[INFO] Attempting to connect to the network...")
    flag = load_config()
    if flag:
        attempt_connection()
        data_setup()
        update_all_connections()
    else:
        print("[ERROR] Failed to connect to the network.")


# Start the server in a separate thread
server_thread = threading.Thread(target=start_server_thread)
server_thread.start()
root = Tk()
root.title("2L-MODS")
root.geometry("800x800")

user_status = Label(root, text="Initializing...\n")
connection_status_label = Label(root, text="Status: 🔴 Disconnected")
connect_button = Button(root, text="Join the Network", command=join_network)

id_label = Label(root, text="ID")
id_entry = Entry(root, width=50)
message_label = Label(root, text="Message")
message_entry = Entry(root, width=50)
send_button = Button(root, text="Send", command=send_message)

user_status.pack()
connection_status_label.pack()
connect_button.pack()

id_label.pack()
id_entry.pack()
message_label.pack()
message_entry.pack()
send_button.pack()

observe_server_port_change()

root.mainloop()
