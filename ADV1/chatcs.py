from socket import socket, SOL_SOCKET, SO_REUSEADDR
from threading import Thread, Lock

# Below modules are created by the author.
from tcpcs import checkPort
from dec import YELLOW, LIGHT_WHITE, END
import messageFunc

BUFFER=2048

## This function executes the appropriate function based on the user's choice.
def ChatServerAndClient(ip, port):
    port = checkPort(port)
    if port != False:
        global host_port
        host_port = (ip, port)
        messageFunc.serviceList()
        try:
            try:
                try:
                    options = int(input(">> "))
                    match options:
                        case 1:
                            chatServer(host_port)
                        case 2:
                            chatClient(host_port)
                        case _:
                            messageFunc.invalidOpt()
                except EOFError:
                    messageFunc.toolKitAborted()
            except ValueError:
                messageFunc.invalidOpt()
        except KeyboardInterrupt:
            messageFunc.toolKitAborted()

# Chat Server Code

def chatServer(host_port):
    CLIENT_LOCK = Lock() ## This will prevent multiple threads from modifying shared data at the same time.
    CLIENT_LIST = [] ## This will add the connected client socket.

## Broadcast the message to all connected clients, excluding the current socket.
    def broadcastMsg(message, sender=None):
        msg=f"{message}\n".encode()

        with CLIENT_LOCK:
            clients = list(CLIENT_LIST)
        
        for client in clients:
            if client is sender:
                continue
            try:
                client.sendall(msg)
            except OSError:
                removeClient(client)

## Safe removal of the client thread.
    def removeClient(client_socket):
        with CLIENT_LOCK:
            if client_socket in CLIENT_LIST:
                CLIENT_LIST.remove(client_socket)
        try:
            client_socket.close()
        except OSError:
            pass

## The main "ClientThread()" handles multiple clients connecting to the server,
## by creating a separate thread for each client.
    class ClientThread(Thread):
        def __init__(self, c_socket, c_address):
            super().__init__(daemon=True) # This will terminate the program even if the thread hasn't finished its task.
            self.c_socket=c_socket
            self.c_address=c_address
            self.c_name = None

        def run(self):
            try:
                self.c_socket.sendall(b"Enter your name: ")
                name=self.c_socket.recv(BUFFER).decode().rstrip()

                if name =='/skip':
                    self.c_name="(Anonymous)"
                elif not name:
                    print(f"Client got disconnected from {self.c_address[0]}:{self.c_address[1]}")
                    return
                else:
                    self.c_name=name

                with CLIENT_LOCK:
                    CLIENT_LIST.append(self.c_socket)

                print(f"[{self.c_name}] joined from {self.c_address[0]}:{self.c_address[1]}")
                self.c_socket.sendall(f"Welcome to chat server {self.c_name}! Type a message and click Enter.\nType quit or exit to leave the chat.\n\n".encode())
                broadcastMsg(f'*** {self.c_name} has joined the chat ***', self.c_socket)

                while True:
                    msg = self.c_socket.recv(BUFFER)
                    if not msg:
                        break
                    if msg:
                        msg = msg.decode().rstrip()
                        if msg.lower() == '/quit' or msg.lower() == '/exit':
                            removeClient(self.c_socket)
                        broadcastMsg(f"{LIGHT_WHITE}[{self.c_name}]{END} {msg}", self.c_socket)
            except OSError:
                pass
            finally:
                removeClient(self.c_socket)
                if self.c_name:
                    print(f"[{self.c_name}] left the chat")
                    broadcastMsg(f"*** {self.c_name} left the chat ***")
                    
## Main code for server
    def main():
        with socket() as server_socket:
            try:
                try:
                    try:
                        server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                        server_socket.bind(host_port)
                        server_socket.listen()
                        messageFunc.serverListening('Chat Application', host_port)
                        while True:
                            client_socket, client_address = server_socket.accept()
                            print(f"Client connected from {client_address[0]}:{client_address[1]}")
                            ClientThread(client_socket, client_address).start()
                    except KeyboardInterrupt:
                        messageFunc.serverShutting('Chat Application')
                    finally:
                        with CLIENT_LOCK:
                            clients = list(CLIENT_LIST)
                        for client in clients:
                            removeClient(client)
                except PermissionError:
                    messageFunc.registeredPort(host_port[1])
            except OSError:
                messageFunc.serverUsedPort(host_port[1])
    main()


## Chat Client Code
def chatClient(host_port):
### Thread is for receiving data from the server
    class ReceivingThread(Thread):
        def __init__(self, socket):
            super().__init__(daemon=True)
            self.socket = socket

        def run(self):
            try:
                while True:
                    server_msg = self.socket.recv(BUFFER)
                    if server_msg:
                        server_msg = server_msg.decode()
                        print(server_msg, end="")
            except OSError:
                self.socket.close()

## Main code for client
    def main():
        try:
            try:
                with socket() as client_socket:
                    client_socket.connect(host_port)
                    print(f"Connecting to chat server...\n\n{YELLOW}[Note]: If you don't see any prompt, hit [enter]{END}\n")
                    ReceivingThread(client_socket).start()
                    while True:
                        data = input()
                        if data.lower() == '/exit' or data.lower() == '/quit':
                            messageFunc.clientQuit(host_port)
                            break
                        client_socket.sendall(data.encode())
            except KeyboardInterrupt:
                messageFunc.clientQuit(host_port)
            finally:
                client_socket.close()
        except ConnectionRefusedError:
            messageFunc.serverWarning()
    main()