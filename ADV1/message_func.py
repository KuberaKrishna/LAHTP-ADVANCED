from dec import (
    BLINK,
    BOLD,
    END,
    GREEN,
    LIGHT_BLUE,
    LIGHT_GRAY,
    LIGHT_GREEN,
    LIGHT_RED,
    LIGHT_YELLOW,
    RED,
    YELLOW,
)

# All these functions
# are used to avoid repeating
# the `print` statement multiple times.


# General Message
def welcome_msg():
    """
    Displays welcome message.
    """
    print(f"{LIGHT_GRAY} ██████ ▄████▄ ▄█████ ██  ██ ▄█████ ▄████▄")
    print(" █▄▄▄▄▄ ██  ██ ██     ██▄█▀  ██▄▄     ██ ")
    print(" ▀▀▀▀██ ██  ██ ██     ██▀█▄  ██▀▀     ██")
    print(" ██████ ▀████▀ ▀█████ ██  ██ ▀█████   ██")
    print()
    print(
        " ▄████▄ ▄████▄ ▄████▄ ▄█████"
        "▄████▄   ███   ▄█▄ ▄█▄ ▄█▄ ▄█▄ "
        "██ ▄█▄  █▄ ▄█████"
    )
    print(
        " ██  ██ ██  ██ ██  ██ ██ ▄▄▄"
        "██  ██  ██ ██  ██▀█▀██ ██▀█▀██ "
        "██ ██▀█ ██ ██ ▄▄▄"
    )
    print(
        " █████▀ █████▀ ██  ██ ██ ▀ █"
        "█████▀ ██▀▀▀██ ██ ▀ ██ ██ ▀ ██ "
        "██ ██ █▄██ ██ ▀ █"
    )
    print(
        " ██     ██ ▀█▄ ▀████▀ ▀█████"
        "██ ▀█▄  ██ ██  ▀█   █▀ ▀█   █▀ "
        "██ ▀█  ██▀ ▀█████"
    )
    print()
    print(" ▄████▄ ▄████▄ ▄████▄ ▄█     ██  ██  ██ ▄████▄")
    print("   ██   ██  ██ ██  ██ ██     ██▄█▀   ██   ██")
    print("   ██   ██  ██ ██  ██ ██     ██▀█▄   ██   ██")
    print(f"   ██   ▀████▀ ▀████▀ ▀█████ ██  ██  ██   ██{END}")


def tool_kit():
    """
    Displays all the tool-kit available.
    """
    available_toolkit = [
        "[0] Port Scanner",
        "[1] Banner Grabber",
        "[2] TCP Client/Server",
        "[3] UDP Client/Server",
        "[4] Chat Application",
    ]
    print(f"\n\n {BOLD}Select one of the options:{END}")
    for tool in available_toolkit:
        print(f"   {BOLD}{tool}{END}")
    print()


def invalid_arg():
    """
    Displays an error message when an invalid argument is selected.
    """
    print()
    print("x-" * 26, end="x\n")
    print(f"\n\t{RED}Invalid arguement valued passed!{END}\n")
    print("x-" * 26, end="x\n\n")


def invalid_opt():
    """
    Displays an error message when an invalid option is selected.
    """
    print()
    print("x-" * 24, end="x\n")
    print(f"\n\t{RED}Invalid options valued passed!{END}\n")
    print("x-" * 24, end="x\n\n")


def unwanted_opt():
    """
    Displays a warning message when an invalid option is selected.
    """
    print("*-" * 27, end="*\n")
    print(f"\n\t{LIGHT_YELLOW}Unwanted options were specified ['-F'].{END}\n")
    print("*-" * 27, end="*\n\n")


def service_list():
    """
    Displays the available service options: server and client.
    """
    print(f"\n{BOLD}[1]Server Listening\n[2]Client Connecting{END}\n")


def toolkit_aborted():
    """
    Displays an error message when Toolkit stops abruptly.
    """
    print()
    print("x-" * 17, end="x\n")
    print(f"\n\t{RED}Toolkit {BLINK}aborted!!{END}\n")
    print("x-" * 17, end="x\n\n")


# Port Message
def registered_port(port_no):
    """
    Displays an error message when the client specifies a known ports.

    Args:
        port_no (int): The registered port.
    """
    print()
    print("x-" * 35, end="x\n")
    print(
        f"\n\t{RED}Server didn't start! You mentioned well-known port '"
        f"{port_no}'\n\t\tthat you don't have permission to use.{END}\n"
    )
    print("x-" * 35, end="x\n\n")


def server_used_port(port_no):
    """
    Displays a warning message, when the client specifies ports
    that are already listening.

    Args:
        port_no (int): The port number already in use.
    """
    print("x-" * 30, end="x\n")
    print(
        f"\n\t{YELLOW}Check whether any other server is running on the\n\t\t"
        f"same port you specified: [{port_no}]\n{END}"
    )
    print("x-" * 30, end="x\n\n")


def invalid_port():
    """
    Displays an error message when the specified ports are outside
    the valid port range.
    """
    print()
    print("x-" * 35, end="x\n")
    print(
        f"\n\t{RED}Ports specified must be between 0 and 65535 "
        f"inclusive\n\t\t\t{BLINK}QUITTING!{END}\n"
    )
    print("x-" * 35, end="x\n\n")


def port_greater(s_port_no, e_port_no):
    """
    Displays a warning when the starting port exceeds the ending port.

    Args:
        s_port_no (int): Starting port number.
        e_port_no (int): Ending port number.
    """
    print("x-" * 32, end="x\n")
    print(
        f"\n\t{LIGHT_RED}Starting port [{s_port_no}] is greater "
        f"than [{e_port_no}] ending.{END}\n"
    )
    print("x-" * 32, end="x\n\n")


def no_port_mentioned():
    """
    Displays an error message when the client does not specify a port.
    """
    print()
    print("x-" * 25, end="x\n")
    print(f"\n\t{RED}Check whether a port is mentioned.{END}\n")
    print("x-" * 25, end="x\n\n")


# IP Message
def invalid_ip():
    """
    Displays an error message when the port exceeds the range.
    """
    print()
    print("x-" * 32, end="x\n")
    print(
        f"\n\t{RED}IPv4 address specified must be between 0 and 255,\n\t\t"
        f"should only be numbers.\n\t\t\t{BLINK}QUITTING!{END}\n"
    )
    print("x-" * 32, end="x\n\n")


# Server Message
def server_init(service_name):
    """
    Display a server-started message.

    Args:
        service_name (str): Service name.
    """
    print()
    print("#-" * 27, end="#\n")
    print(f"\n\t{service_name} server initiated ...\n")
    print("#-" * 27, end="#\n")


def server_listening(service_name, host_port):
    """
    Displays a server-listening message.

    Args:
        service_name (str): Service name.
        host_port (str)t: Server's IP and Port
    """
    print(
        f"\n{GREEN}{service_name} Server Started Listening on {host_port[0]} "
        f"{host_port[1]}{END}\n"
    )


def received_msg(client_address, message):
    """
    Displays the message received from the client.

    Args:
        client_address (tuple): Client's IP address and port number.
        message (str): Message received from the client.
    """
    print(f"Received from [{client_address}]: {message}")


def server_warning():
    """
    Displays a warning message when the server fails to start.
    """
    print("*-" * 27, end="*\n")
    print(f"\n\t{YELLOW}Check whether the server is running.{END}\n")
    print("*-" * 27, end="*\n\n")


def server_error():
    """
    Displays an error message when a server-side problem occurs.
    """
    print("x-" * 30, end="x\n")
    print(f"\n\t{RED}500 Internal Server Error{END}\n")
    print(
        f"{YELLOW}[Error brief]: The server may be offline "
        f"or unavailable.{END}"
    )
    print("x-" * 30, end="x\n\n")


def server_shutting(service_name):
    """
    Displays a message when shutting down a particular service.

    Args:
        service_name (str): Service name.
    """
    print()
    print("x-" * 27, end="x\n")
    print(f"\n\t{LIGHT_GREEN}{service_name} server shutting down ...{END}\n")
    print("x-" * 27, end="x\n\n")


# Client Message
def client_quit(host_port):
    """
    Displays a message when the client disconnects from the server.

    Args:
        host_port (tuple): Client's IP address and port.
    """
    print()
    print("x-" * 27, end="x\n")
    print(
        f"\n\t{LIGHT_BLUE}You quited from the server "
        f"{host_port[0]}:{host_port[1]}{END}\n"
    )
    print("x-" * 27, end="x\n\n")
