from tkinter import *
from tkinter import messagebox
import server
import client
import threading
import network
import queue


def start_server_thread():
    server.start_server()


def start_client_thread(server_address, result_queue):
    # Connect to the server and get the result
    result = client.connect_to_server(server_address)
    # Put the result in the queue
    result_queue.put(result)


def connect_to_server(server_address):
    # Create a queue to get the return value from the thread
    result_queue = queue.Queue()
    # Start a new client connection in a separate thread
    client_thread = threading.Thread(
        target=start_client_thread, args=(server_address, result_queue)
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
            if current_text == "接続状態: 🔴 未接続":
                current_text = ""
            new_text = (
                current_text + "\n接続状態: 🟢 接続されました (" + server_address + ")"
            )
            connection_status_label.config(text=new_text)
        else:
            # give out an alert on GUI as a message box
            messagebox.showerror(
                "接続エラー",
                "⚠️ 接続に失敗しました。\n\n該当ユーザーが2L-MODSを起動しているか、IPアドレスが正しいかを確認してください。",
            )
            # Clear the entry field
        entry.delete(0, END)


# Start the server in a separate thread
server_thread = threading.Thread(target=start_server_thread)
server_thread.start()

root = Tk()
root.title("2L-MODS")
root.geometry("800x800")

your_ip_and_status_label = Label(
    root, text="あなたのIPアドレス: " + network.get_public_ip() + "\n"
)
connection_status_label = Label(root, text="接続状態: 🔴 未接続")
ip_input_label = Label(root, text="相手のIPアドレスを入力してください。")
entry = Entry(root, width=50)
connect_button = Button(
    root, text="接続", command=lambda: connect_to_server(entry.get())
)

your_ip_and_status_label.pack()
connection_status_label.pack()
ip_input_label.pack()
entry.pack()
connect_button.pack()

root.mainloop()
