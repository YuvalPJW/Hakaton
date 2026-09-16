import socket
import threading

PORT = 5000

SERVER = '0.0.0.0'
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"

clients, names = [], []

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind(ADDRESS)


def start_chat():

    print("server is working on " + SERVER)

    server.listen()

    while True:

        conn, addr = server.accept()
        print(f"New connection request from {addr}")

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


def handle_client(conn, addr):
    try:
        conn.send("NAME".encode(FORMAT))
        name = conn.recv(1024).decode(FORMAT)

        if not name:
            conn.close()
            return

        names.append(name)
        clients.append(conn)

        print(f"Name registered: {name} ({addr})")
        broadcast_message(f"{name} joined the chat!".encode(FORMAT))
        conn.send("Connection successful!\n".encode(FORMAT))

        connected = True
        while connected:
            message = conn.recv(1024)
            if message:
                broadcast_message(message)
            else:
                connected = False
    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        if conn in clients:
            idx = clients.index(conn)
            clients.remove(conn)
            names.pop(idx)
            conn.close()


def broadcast_message(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass

start_chat()