import socket
import threading
from pathlib import Path
from tkinter import *
from PIL import Image, ImageTk


PORT = 5000
SERVER = "10.243.18.79"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"

DEFAULT_USERNAME = "User"

client = None

base_dir = Path(__file__).resolve().parent


def setup_chat_client(parent_frame, username=DEFAULT_USERNAME):

    global client


    # ---------------- CONNECT SOCKET ----------------

    try:
        client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        client.connect(ADDRESS)

    except Exception as error:
        print(f"Error connecting to server: {error}")


    # ---------------- CHAT CONTAINER ----------------

    chat_container = Frame(
        parent_frame,
        bg="#f8f2e8"
    )

    chat_container.pack(
        fill=BOTH,
        expand=True
    )


    # ---------------- BACKGROUND IMAGE ----------------

    background_image = Image.open(
        base_dir / "chat_background.jpeg"
    ).convert("RGB")


    background_label = Label(
        chat_container,
        bd=0
    )

    background_label.place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )


    background_label.original_image = background_image
    background_label.image = None


    def resize_background(event=None):

        width = chat_container.winfo_width()
        height = chat_container.winfo_height()

        if width < 2 or height < 2:
            return


        resized_image = background_label.original_image.resize(
            (width, height),
            Image.Resampling.LANCZOS
        )


        photo = ImageTk.PhotoImage(
            resized_image
        )


        background_label.config(
            image=photo
        )


        background_label.image = photo


    chat_container.bind(
        "<Configure>",
        resize_background
    )


    # ---------------- HEADER ----------------

    label_head = Label(
        chat_container,
        text=f"Chatroom ({username})",
        font=("Helvetica", 15, "bold"),
        fg="black",
        bg="#fffaf2",
        pady=8
    )

    label_head.pack(
        fill=X,
        padx=15,
        pady=(15, 5)
    )


    # ---------------- CHAT DISPLAY ----------------

    text_frame = Frame(
        chat_container,
        bg="#fffaf2"
    )

    text_frame.pack(
        fill=BOTH,
        expand=True,
        padx=15,
        pady=5
    )


    scrollbar = Scrollbar(
        text_frame
    )

    scrollbar.pack(
        side=RIGHT,
        fill=Y
    )


    text_cons = Text(
        text_frame,
        bg="#fffaf2",
        fg="black",
        insertbackground="black",
        font=("Helvetica", 12),
        yscrollcommand=scrollbar.set,
        wrap=WORD,
        relief="flat",
        bd=0,
        padx=10,
        pady=10
    )

    text_cons.pack(
        side=LEFT,
        fill=BOTH,
        expand=True
    )


    scrollbar.config(
        command=text_cons.yview
    )


    text_cons.config(
        state=DISABLED
    )


    # ---------------- INPUT BAR ----------------

    input_frame = Frame(
        chat_container,
        bg="#fffaf2"
    )

    input_frame.pack(
        fill=X,
        padx=15,
        pady=(5, 15)
    )


    entry_msg = Entry(
        input_frame,
        bg="white",
        fg="black",
        insertbackground="black",
        font=("Helvetica", 12),
        relief="solid",
        bd=1
    )

    entry_msg.pack(
        side=LEFT,
        fill=X,
        expand=True,
        padx=(0, 8),
        pady=8,
        ipady=8
    )


    # ---------------- RECEIVE ----------------

    def receive():

        while True:

            try:

                message = client.recv(
                    1024
                ).decode(
                    FORMAT
                )


                if message == "NAME":

                    client.send(
                        username.encode(
                            FORMAT
                        )
                    )


                else:

                    text_cons.config(
                        state=NORMAL
                    )


                    text_cons.insert(
                        END,
                        message + "\n\n"
                    )


                    text_cons.config(
                        state=DISABLED
                    )


                    text_cons.see(
                        END
                    )


            except Exception:

                print(
                    "Disconnected from server."
                )


                if client:

                    client.close()


                break


    # ---------------- SEND ----------------

    def send_message(event=None):

        message = entry_msg.get()


        if not message:
            return


        entry_msg.delete(
            0,
            END
        )


        def raw_send():

            try:

                client.send(
                    f"{username}: {message}".encode(
                        FORMAT
                    )
                )


            except Exception as error:

                print(
                    f"Failed to send: {error}"
                )


        threading.Thread(
            target=raw_send,
            daemon=True
        ).start()


    entry_msg.bind(
        "<Return>",
        send_message
    )


    # ---------------- SEND BUTTON ----------------

    send_button = Button(
        input_frame,
        text="Send",
        font=("Helvetica", 10, "bold"),
        bg="#e6d7bd",
        fg="black",
        activebackground="#d8c5a6",
        activeforeground="black",
        bd=0,
        padx=15,
        pady=8,
        command=send_message
    )

    send_button.pack(
        side=RIGHT
    )


    # ---------------- KEEP WIDGETS ABOVE BACKGROUND ----------------

    background_label.lower()

    label_head.lift()

    text_frame.lift()

    input_frame.lift()


    # ---------------- START LISTENER ----------------

    rcv_thread = threading.Thread(
        target=receive,
        daemon=True
    )

    rcv_thread.start()