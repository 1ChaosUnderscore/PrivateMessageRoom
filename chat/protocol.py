import json
import subprocess
import os

class JSONSocket:
    def __init__(self, sock):
        self.sock = sock
        self.buffer = ""

    def receive(self):
        while True:
            if "\n" in self.buffer:
                line, self.buffer = self.buffer.split("\n", 1)
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    continue
            chunk = self.sock.recv(1024).decode()
            if not chunk:
                return None
            self.buffer += chunk

    def send(self, data):
        message = json.dumps(data) + "\n"
        self.sock.sendall(message.encode())

def receiveJSON(sock):
    return JSONSocket(sock).receive()

def sendJSON(sock, data):
    JSONSocket(sock).send(data)

def clear_screen():
    if os.name == 'nt':
        subprocess.run("cls", shell=True)
    else:
        try:
            subprocess.run("/usr/bin/clear")
        except FileNotFoundError:
            subprocess.run("clear")