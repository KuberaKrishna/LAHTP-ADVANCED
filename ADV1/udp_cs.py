from socket import AF_INET, SOCK_DGRAM, socket

# Below modules are created by the author.
import message_func
from dec import END, LIGHT_WHITE
from tcp_cs import check_port

BUFFER = 2048


def socket_connection_gram(ip, port_no):
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
        except ValueError:
            message_func.invalid_opt()
        except (KeyboardInterrupt, EOFError):
            message_func.toolkit_aborted()


# Socket Code
# Server Socket code


def socket_server(host_port):
    """
    Main function for starting the server socket.
    This is (optional).

    Args:
        host_port (tuple): Server's listening IPv4 address and port number.
    """
    try:
        with socket(AF_INET, SOCK_DGRAM) as server_socket:
            server_socket.bind(host_port)
            message_func.server_listening("UDP", host_port)
            while True:
                data, client_address = server_socket.recvfrom(BUFFER)
                message = data.decode().rstrip()
                message_func.received_msg(client_address[0], message)
    except KeyboardInterrupt:
        message_func.server_shutting("UDP")
    except PermissionError:
        message_func.registered_port(host_port[1])
    except OSError:
        message_func.server_used_port(host_port[1])


# Client socket code


def client_socket(host_port):
    """
    Main function for starting the client socket.

    Args:
        host_port (tuple): Client's  IPv4 address and port number.
    """
    print()
    try:
        with socket(AF_INET, SOCK_DGRAM) as client_socket:
            while True:
                data = input(f"{LIGHT_WHITE}Enter something:{END} ")
                if data.lower() == "/quit" or data.lower() == "/exit":
                    message_func.client_quit(host_port)
                    break
                client_socket.sendto(data.encode("utf-8"), host_port)
    except KeyboardInterrupt:
        message_func.client_quit(host_port)
