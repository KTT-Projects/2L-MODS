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
        new_text = (
            f"{current_text}\nStatus: 🟢 Connected to {server_address} : {port_number}"
        )
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
    if server.port != -1:
        user_status.config(
            text=f"Listening on {server.server_address} : {server.port}\n"
        )
        return
    # Schedule the next observation
    root.after(100, observe_server_port_change)


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

user_status.pack()
connection_status_label.pack()
ip_input_label.pack()
entry.pack()
port_label.pack()
port_entry.pack()
connect_button.pack()

# Start observing the server.port variable
observe_server_port_change()

root.mainloop()
