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

        # Start a handler thread to perform handshake & receive messages
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        #
        # conn.send("NAME".encode(FORMAT))
        #
        # name = conn.recv(1024).decode(FORMAT)
        #
        # names.append(name)
        # clients.append(conn)
        #
        # print(f"Name is :{name}")
        #
        # # broadcast message
        # broadcast_message(f"{name} has joined the chat!".encode(FORMAT))
        #
        # conn.send('Connection successful!'.encode(FORMAT))
        #
        # # Start the handling thread
        # thread = threading.Thread(target=handle,
        #                           args=(conn, addr))
        # thread.start()
        #
        # # no. of clients connected
        # # to the server
        # print(f"active connections {threading.activeCount()-1}")

# method to handle the
# incoming messages

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


# if __name__ == "__main__":
#     start_chat()
#
# def handle(conn, addr):
#
#     print(f"new connection {addr}")
#     connected = True
#
#     while connected:
#           # receive message
#         message = conn.recv(1024)
#
#         # broadcast message
#         broadcast_message(message)
#
#     # close the connection
#     conn.close()
#
# # method for broadcasting
# # messages to each client
#
#
# def broadcast_message(message):
#     for client in clients:
#         client.send(message)
#

# call the method to
# begin the communication
start_chat()