
import socket
import threading
from tkinter import *

PORT = 5000
SERVER = "10.121.140.101"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"

# Set your default username here
DEFAULT_USERNAME = "User"

client = None


def setup_chat_client(parent_frame, username=DEFAULT_USERNAME):
    """Initializes the socket and directly builds the chat UI inside parent_frame."""
    global client

    # 1. Connect socket
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDRESS)
    except Exception as e:
        print(f"Error connecting to server: {e}")

    # 2. Build Chat Layout directly inside parent_frame (leftFrame)
    chat_container = Frame(parent_frame, bg="#17202A")
    chat_container.pack(fill=BOTH, expand=True)

    # Header
    labelHead = Label(
        chat_container,
        bg="#17202A",
        fg="#EAECEE",
        text=f"Chatroom ({username})",
        font=("Helvetica", 13, "bold"),
        pady=8,
    )
    labelHead.pack(fill=X)

    # Chat Display
    text_frame = Frame(chat_container, bg="#17202A")
    text_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

    scrollbar = Scrollbar(text_frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    textCons = Text(
        text_frame,
        bg="#17202A",
        fg="#EAECEE",
        font=("Helvetica", 12),
        yscrollcommand=scrollbar.set,
        wrap=WORD,
    )
    textCons.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.config(command=textCons.yview)
    textCons.config(state=DISABLED)

    # Input Bar
    input_frame = Frame(chat_container, bg="#ABB2B9", pady=5)
    input_frame.pack(fill=X, side=BOTTOM)

    entryMsg = Entry(
        input_frame, bg="#2C3E50", fg="#EAECEE", font=("Helvetica", 12)
    )
    entryMsg.pack(side=LEFT, fill=X, expand=True, padx=5)

    def receive():
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
                # Respond to server's name request
                if message == "NAME":
                    client.send(username.encode(FORMAT))
                else:
                    textCons.config(state=NORMAL)
                    textCons.insert(END, message + "\n\n")
                    textCons.config(state=DISABLED)
                    textCons.see(END)
            except:
                print("Disconnected from server.")
                if client:
                    client.close()
                break

    def send_message(event=None):
        msg = entryMsg.get()
        if not msg:
            return
        entryMsg.delete(0, END)

        def _raw_send():
            try:
                client.send(f"{username}: {msg}".encode(FORMAT))
            except Exception as e:
                print(f"Failed to send: {e}")

        threading.Thread(target=_raw_send, daemon=True).start()

    # entryMsg.bind("", send_message)

    send_btn = Button(
        input_frame,
        text="Send",
        font=("Helvetica", 10, "bold"),
        bg="#ABB2B9",
        command=send_message,
    )
    send_btn.pack(side=RIGHT, padx=5)

    # 3. Start background listener thread
    rcv_thread = threading.Thread(target=receive, daemon=True)
    rcv_thread.start()