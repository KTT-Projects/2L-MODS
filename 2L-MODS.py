from tkinter import *
import server
import client
import threading


def start_server_thread():
    server.start_server()


# Start the server in a separate thread
server_thread = threading.Thread(target=start_server_thread)
server_thread.start()

root = Tk()
root.title("2L-MODS")
root.geometry("800x800")

Label(root, text="相手のIPアドレスを入力").pack()
entry = Entry(root, width=50)
button = Button(root, text="接続", command=lambda: print(entry.get()))

entry.pack()
button.pack()

root.mainloop()
