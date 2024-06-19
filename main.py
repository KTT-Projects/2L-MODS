from tkinter import *
from tkinter import messagebox
import server
import client
import threading
import network
import queue


def start_server_thread():
    server.start_server()


def start_client_thread(server_address, port_number, result_queue):
    # Connect to the server and get the result
    result = client.connect_to_server(server_address, port_number)
    # Put the result in the queue
    result_queue.put(result)


def connect_to_server(server_address, port_number):
    # Create a queue to get the return value from the thread
    result_queue = queue.Queue()
    # Start a new client connection in a separate thread
    client_thread = threading.Thread(
        target=start_client_thread, args=(server_address, port_number, result_queue)
    )
    client_thread.start()
    # Check the connection status periodically
    root.after(100, check_connection_status, result_queue, server_address)


def check_connection_status(result_queue, server_address):
    if result_queue.empty():
        # If the result queue is empty, check again after 100ms
        root.after(100, check_connection_status, result_queue, server_address)
    else:
        result = result_queue.get()
        # Update the connection status label based on the result
        if result:
            current_text = connection_status_label.cget("text")
            if current_text == "Status: 🔴 Disconnected":
                current_text = ""
            new_text = f"{current_text}\nStatus: 🟢 Connected to {server_address} : {port_entry.get()}"
            connection_status_label.config(text=new_text)
            # Clear the entry fields
            entry.delete(0, END)
            port_entry.delete(0, END)
        else:
            # give out an alert on GUI as a message box
            messagebox.showerror(
                "Connection Error",
                "⚠️ Connection Failed\n\nPlease check the IP address and try again.",
            )


def observe_server_port_change():
    # Check for changes in the server.port variable
    if server.port != -1:
        user_status.config(
            text=f"Listening on {server.server_address} : {server.port}\n"
        )
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
    command=lambda: connect_to_server(entry.get(), port_entry.get()),
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
