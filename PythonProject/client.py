
import socket
import threading
from tkinter import *

PORT = 5000
SERVER = "10.243.18.79"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"

DEFAULT_USERNAME = "User"

client = None


def setup_chat_client(parent_frame, username=DEFAULT_USERNAME):
    global client

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDRESS)
    except Exception as e:
        print(f"Error connecting to server: {e}")

    chat_container = Frame(parent_frame, bg="#17202A")
    chat_container.pack(fill=BOTH, expand=True)

    labelHead = Label(
        chat_container,
        bg="#17202A",
        fg="#EAECEE",
        text=f"Chatroom ({username})",
        font=("Helvetica", 13, "bold"),
        pady=8,
    )
    labelHead.pack(fill=X)

    text_frame = Frame(chat_container, bg="#17202A")
    text_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

    scrollbar = Scrollbar(text_frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    text_cons = Text(
        text_frame,
        bg="#17202A",
        fg="#EAECEE",
        font=("Helvetica", 12),
        yscrollcommand=scrollbar.set,
        wrap=WORD,
    )
    text_cons.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.config(command=text_cons.yview)
    text_cons.config(state=DISABLED)

    input_frame = Frame(chat_container, bg="#ABB2B9", pady=5)
    input_frame.pack(fill=X, side=BOTTOM)

    entry_msg = Entry(
        input_frame, bg="#2C3E50", fg="#EAECEE", font=("Helvetica", 12)
    )
    entry_msg.pack(side=LEFT, fill=X, expand=True, padx=5)

    def receive():
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
                # Respond to server's name request
                if message == "NAME":
                    client.send(username.encode(FORMAT))
                else:
                    text_cons.config(state=NORMAL)
                    text_cons.insert(END, message + "\n\n")
                    text_cons.config(state=DISABLED)
                    text_cons.see(END)
            except:
                print("Disconnected from server.")
                if client:
                    client.close()
                break

    def send_message(event=None):
        msg = entry_msg.get()
        if not msg:
            return
        entry_msg.delete(0, END)

        def _raw_send():
            try:
                client.send(f"{username}: {msg}".encode(FORMAT))
            except Exception as e:
                print(f"Failed to send: {e}")

        threading.Thread(target=_raw_send, daemon=True).start()

    entry_msg.bind("<Return>", send_message)

    send_btn = Button(
        input_frame,
        text="Send",
        font=("Helvetica", 10, "bold"),
        bg="#ABB2B9",
        command=send_message,
    )
    send_btn.pack(side=RIGHT, padx=5)

    rcv_thread = threading.Thread(target=receive, daemon=True)
    rcv_thread.start()