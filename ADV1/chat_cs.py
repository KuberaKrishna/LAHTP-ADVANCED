from socket import SO_REUSEADDR, SOL_SOCKET, socket
from threading import Lock, Thread

# Below modules are created by the author.
import message_func
from dec import END, LIGHT_WHITE
from tcp_cs import check_port

BUFFER = 2048


def chat_server_client(ip, port_no):
    """
    This function executes the appropriate function based on the user's choice.

    Args:
        ip (str): The server's IPv4 address.
        port_no (str): The servers's listening port number.
    """
    port_no = check_port(port_no)
    if port_no is not False:
        global host_port
        host_port = (ip, port_no)
        message_func.service_list()
        try:
            options = int(input(">> "))
            match options:
                case 1:
                    chat_server(host_port)
                case 2:
                    chat_client(host_port)
                case _:
                    message_func.invalid_opt()
        except EOFError:
            message_func.toolkit_aborted()
        except ValueError:
            message_func.invalid_opt()
        except KeyboardInterrupt:
            message_func.toolkit_aborted()


# Chat Server Code


def chat_server(host_port):
    CLIENT_LOCK = Lock()  # Prevent multiple threads from modifying.
    CLIENT_LIST = []  # Added connected client.

    def broadcast_msg(message, sender=None):
        """
        Broadcasts a message to all connected client except the sender.

        Args:
            message (str): The message to send.
            sender (str): The client currently sending the message.
        """
        msg = f"{message}\n".encode()

        with CLIENT_LOCK:
            clients = list(CLIENT_LIST)

        for client in clients:
            if client is sender:
                continue
            try:
                client.sendall(msg)
            except OSError:
                remove_client(client)

    def remove_client(client_socket):
        """
        Safe removal of the client thread.

        Args:
            client_socket: The current client.
        """
        with CLIENT_LOCK:
            if client_socket in CLIENT_LIST:
                CLIENT_LIST.remove(client_socket)
        try:
            client_socket.close()
        except OSError:
            pass

    class ClientThread(Thread):
        """
        Handles multiple clients connecting
        to the server and creates a separate thread
        for each client.

        Args:
            c_socket: The current client_socket.
            c_address: The current client address.
        """

        def __init__(self, c_socket, c_address):
            super().__init__(daemon=True)

            self.c_socket = c_socket
            self.c_address = c_address
            self.c_name = None

        def run(self):
            try:
                self.c_socket.sendall(b"Enter your name: ")
                name = self.c_socket.recv(BUFFER).decode().rstrip()

                if name == "/skip":
                    self.c_name = "(Anonymous)"
                elif not name:
                    print(
                        f"Client got disconnected from"
                        f"{self.c_address[0]}:{self.c_address[1]}"
                    )
                    return
                else:
                    self.c_name = name

                with CLIENT_LOCK:
                    CLIENT_LIST.append(self.c_socket)

                print(
                    f"[{self.c_name}] joined from "
                    f"{self.c_address[0]}:{self.c_address[1]}"
                )
                self.c_socket.sendall(
                    f"Welcome to chat server {self.c_name}!"
                    f"Type a message and click Enter.\n"
                    f"Type /quit or /exit to leave the chat.\n\n".encode()
                )
                broadcast_msg(
                    f"*** {self.c_name} has joined"
                    f"the chat ***", self.c_socket
                )

                while True:
                    msg = self.c_socket.recv(BUFFER)
                    if not msg:
                        break
                    if msg:
                        msg = msg.decode().rstrip()
                        if msg.lower() == "/quit" or msg.lower() == "/exit":
                            remove_client(self.c_socket)
                        broadcast_msg(
                            f"{LIGHT_WHITE}[{self.c_name}]{END} {msg} ",
                            self.c_socket
                        )
            except OSError:
                pass
            finally:
                remove_client(self.c_socket)
                if self.c_name:
                    print(f"[{self.c_name}] left the chat")
                    broadcast_msg(f"*** {self.c_name} left the chat ***")

    def chat_server_main():
        """
        Establishing the server.
        """
        with socket() as server_socket:
            try:
                server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                server_socket.bind(host_port)
                server_socket.listen()
                message_func.server_listening("Chat Application", host_port)
                while True:
                    client_socket, client_address = server_socket.accept()
                    print(
                        f"Client connected from "
                        f"{client_address[0]}:{client_address[1]}"
                    )
                    client_socket.sendall(b"\n")
                    ClientThread(client_socket, client_address).start()
            except PermissionError:
                message_func.registered_port(host_port[1])
            except OSError:
                message_func.server_used_port(host_port[1])
            except KeyboardInterrupt:
                message_func.server_shutting("Chat Application")
            finally:
                with CLIENT_LOCK:
                    clients = list(CLIENT_LIST)
                for client in clients:
                    remove_client(client)

    chat_server_main()


# Chat client code


def chat_client(host_port):

    class ReceivingThread(Thread):
        """
        Receives data from the server.

        Args:
            socket: The current client socket.
        """

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

    def chat_client_main():
        """
        Establishing the client.
        """
        try:
            with socket() as client_socket:
                client_socket.connect(host_port)
                ReceivingThread(client_socket).start()
                while True:
                    data = input()
                    if data.lower() == "/exit" or data.lower() == "/quit":
                        message_func.client_quit(host_port)
                        break
                    client_socket.sendall(data.encode())
        except ConnectionRefusedError:
            message_func.client_quit(host_port)
        except KeyboardInterrupt:
            message_func.server_warning()
        finally:
            client_socket.close()

    chat_client_main()
