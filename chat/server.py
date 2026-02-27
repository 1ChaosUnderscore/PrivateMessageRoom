import socket
import threading
from protocol import JSONSocket, clear_screen

clear_screen()

clients = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    server.bind(("0.0.0.0", 5555))
    print("Server Started")
except Exception as e:
    print("Unknown Error: ", e)
server.listen()

def broadcast(data, sender):
    for connection in clients:
        if connection != sender:
            connection.send(data)

def handleClient(connection, addr):
    while True:
        data = connection.receive()
        if not data:
            break
        if data["type"] == "message":
            broadcast(data, connection)
        elif data["type"] == "join":
            broadcast({
                "type": "system",
                "content": f"\r\033[K{data["user"]} joined the room"
            }, connection)
        elif data["type"] == "leave":
            broadcast({
                "type": "system",
                "content": f"\r\033[K{data["user"]} left the room"
            }, connection)
            print(f"User disconnected from {addr}")
    clients.remove(connection)
    connection.sock.close()

def acceptClients():
    while True:
        try:
            client, addr = server.accept()
        except KeyboardInterrupt:
            print("\Server Connection Ended")
            break
        except Exception as e:
            print("Disconnected:", e)
            continue
        print(f"User connected from {addr}")
        connection = JSONSocket(client)
        clients.append(connection)
        thread = threading.Thread(target=handleClient, args=(connection, addr))
        thread.start()
    server.close()

def getAddr():
    return 

acceptClients()