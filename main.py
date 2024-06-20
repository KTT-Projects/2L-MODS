from tkinter import *
from tkinter import messagebox
import server
import client
import threading
import network
import queue


def start_server_thread():
    server.start_server()


def start_client_thread(server_address, port_number):
    client.connect_to_server(server_address, port_number)


def connect_to_server(server_address, port_number):
    if (server_address, port_number, "Connected") in client.connections:
        messagebox.showerror(
            "Connection Error",
            "⚠️ Already Connected\n\nYou are already connected to this server.",
        )
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
        entry.delete(0, END)
        port_entry.delete(0, END)
    elif (server_address, port_number, "Failed") in client.connections:
        messagebox.showerror(
            "Connection Error",
            "⚠️ Connection Failed\n\nPlease check the IP address and try again.",
        )
        client.connections.remove((server_address, port_number, "Failed"))
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


# Start the server in a separate thread
server_thread = threading.Thread(target=start_server_thread)
server_thread.start()

root = Tk()
root.title("2L-MODS")
root.geometry("800x800")

user_status = Label(root, text="Initializing...\n")
connection_status_label = Label(root, text="Status: 🔴 Disconnected")
ip_input_label = Label(root, text="Enter other IP address below")
entry = Entry(root, width=50)
port_label = Label(root, text="Port Number")
port_entry = Entry(root, width=50)
connect_button = Button(
    root,
    text="Connect",
    command=lambda: connect_to_server(entry.get(), int(port_entry.get())),
)

id_label = Label(root, text="ID")
id_entry = Entry(root, width=50)
message_label = Label(root, text="Message")
message_entry = Entry(root, width=50)
send_button = Button(root, text="Send", command=send_message)

user_status.pack()
connection_status_label.pack()
ip_input_label.pack()
entry.pack()
port_label.pack()
port_entry.pack()
connect_button.pack()

id_label.pack()
id_entry.pack()
message_label.pack()
message_entry.pack()
send_button.pack()

# Start observing the server.port variable
observe_server_port_change()

root.mainloop()
