from re import search
from socket import SO_REUSEADDR, SOL_SOCKET, socket

# Below modules are created by the author.
import message_func
from dec import END, GREEN, LIGHT_WHITE

BUFFER = 2048


def check_port(port_no):
    """
    Checks whether a port number is valid for listening or connecting.

    Args:
        port_no (str): User-provided port number.
    """
    try:
        port_pattern = r"^(?:6553[0-5]|655[0-2]\d|65[0-4]\d{2}|\
            6[0-4]\d{3}|[1-5]\d{4}|[1-9]\d{0,3}|0)$"
        if search(port_pattern, port_no):
            return int(port_no)
        else:
            message_func.invalid_port()
            return False
    except TypeError:
        message_func.no_port_mentioned()


def socket_connection_stream(ip, port_no):
    """
    Executes the appropriate function based on the user's choice.

    Args:
        ip (str): User-provided IPv4 address.
        port_no (int): User-provided port number.
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
                    socket_server(host_port)
                case 2:
                    client_socket(host_port)
                case _:
                    message_func.invalid_opt()
        except EOFError:
            message_func.toolkit_aborted()
        except ValueError:
            message_func.invalid_opt()
        except KeyboardInterrupt:
            message_func.toolkit_aborted()


# Socket Code


# Server Socket code
def socket_server(host_port):
    """
    Main function for starting the server socket.

    Args:
        host_port (tuple): Server's listening IPv4 address and port number.
    """
    try:
        with socket() as server_socket:
            server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            server_socket.bind(host_port)
            server_socket.listen()
            message_func.server_listening("TCP", host_port)
            client_socket, client_address = server_socket.accept()

        with client_socket:
            print(
                f"Client connected: "
                f"{client_address[0]}:{client_address[1]}\n"
            )
            client_socket.sendall(
                f"\nConnected to server on port "
                f"{host_port[1]}".encode()
            )
            while True:
                data = client_socket.recv(
                    BUFFER
                )  # can receive data up to 2048 bytes
                if not data:  # no data === client closed connection
                    break
                message = data.decode().rstrip()
                message_func.received_msg(client_address[0], message)
            print(
                f"\nThe client [{client_address[0]}] "
                f"has disconnected from the server."
            )
            message_func.server_shutting("TCP")
    except KeyboardInterrupt:
        message_func.server_shutting("TCP")
    except PermissionError:
        message_func.registered_port(host_port[1])
    except OSError:
        message_func.server_used_port(host_port[1])


# Client socket code
def client_socket(host_port):
    """
    Main function for starting the client socket.

    Args:
        host_port (tuple): Client's IPv4 address and port number.
    """
    try:
        with socket() as client_socket:
            client_socket.connect(host_port)
            srv_msg = client_socket.recv(BUFFER)
            if srv_msg:
                print(f"{GREEN}{srv_msg.decode().rstrip()}{END}")
                while True:
                    data = input(
                        f"{LIGHT_WHITE}"
                        f"Enter something: {END}"
                    )
                    if (
                        data.lower() == "/quit"
                        or data.lower() == "/exit"
                    ):
                        break
                    client_socket.sendall(data.encode())
    except KeyboardInterrupt:
        message_func.client_quit(host_port)
    except BrokenPipeError:
        message_func.server_error()
    except ConnectionRefusedError:
        message_func.server_warning()
