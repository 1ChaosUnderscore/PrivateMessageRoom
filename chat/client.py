import socket
import threading
from protocol import JSONSocket, clear_screen

clear_screen()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(("127.0.0.1", 5555))
    print("Connected")

    connection = JSONSocket(client)
    username = input("Username: ")
    connection.send({
        "type": "join",
        "user": username
    })
except TimeoutError:
    print("Timed Out")
except ConnectionRefusedError:
    print("Connection Refused. Server Is Likely Closed")
except ConnectionError:
    print("Connection Error")
except:
    print("Unknown Error")

current_input = ""

def receive():
    while True:
        data = connection.receive()
        if not data:
            print("\rDisconnected")
            break
        if data["type"] == "message":
            print(f"\r\033[K{data['user']}: {data['content']}")
            print(f"Message: {current_input}", end="", flush=True)
        elif data["type"] == "system":
            print(data["content"])
            print(f"Message: {current_input}", end="", flush=True)

def send():
    global current_input
    while True:
        try:
            current_input = ""
            print("Message: ", end="", flush=True)
            current_input = input()
            data = {
                "type": "message",
                "user": username,
                "content": current_input
            }
            print(f"\033[A\r\033[K{username}: {current_input}")
            connection.send(data)
        except KeyboardInterrupt:
            print("\nProgram Exited")
            connection.send({
                "type": "leave",
                "user": username
            })
            client.close()
            break

threading.Thread(target=receive, daemon=True).start()
send()