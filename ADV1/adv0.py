from argparse import ArgumentParser
from sys import argv

# Below modules are created by the author.
import banner_func
import chat_cs
import message_func
import port_func
import tcp_cs
import udp_cs

message_func.welcome_msg()


def port_scanner(ip, port_no):
    """"
    Main function for scanning the specified ports.

    Args:
        ip (str): The IPv4 address of the target.
        port_no (str): The port or ports to scan.
    """
    if args.Fast and args.port:
        message_func.unwanted_opt()
    else:
        port_func.print_header(ip)
        if not args.port and not args.Fast:
            port_func.all_port(ip)
        elif args.Fast and not args.port:
            port_func.fast_mode(ip)
        else:
            port_func.custom_scan(ip, port_no)
        port_func.print_end()


def banner_grabber(ip, port_no):
    """
    Main function for grabbing banners from the specified ports.

    Args:
        ip (str): The IPv4 address of the target.
        port_no (str): The port or ports to grab banners from.
    """
    if not args.port and not args.Fast:
        banner_func.print_header(ip)
        banner_func.all_banner_grabber(ip)
        banner_func.print_end()
    elif not args.Fast:
        banner_func.print_header(ip)
        banner_func.custom_grabber(ip, port_no)
        banner_func.print_end()
    else:
        message_func.unwanted_opt()


def tcp_client_server(ip, port_no):
    """
    Establishes a TCP connection between a client and server.

    Args:
        ip (str): The IPv4 address of the client or server.
        port_no (str): The port number used for the connection.
    """
    if tcp_cs.check_port(port_no):
        message_func.server_init("TCP")
        tcp_cs.socket_connection_stream(ip, port_no)


def udp_client_server(ip, port_no):
    """
    Main function for UDP client-server communication.

    Args:
        ip (str): The IPv4 address of the client or server.
        port_no (str): The port number used for communication.
   """
    if tcp_cs.check_port(port_no):
        message_func.server_init("UDP")
        udp_cs.socket_connection_gram(ip, port_no)


def chat_client_server(ip, port_no):
    """
    Establishes TCP connections between multiple clients and a server.

    Args:
        ip (str): The IPv4 address of the client or server.
        port_no (str): The port number used for the connections.
    """
    if tcp_cs.check_port(port_no):
        message_func.server_init("Multi Client Chat")
        chat_cs.chat_server_client(ip, port_no)


def distributing_function(options):
    """
    Dispatches functions based on the selected option.

    Args:
        options (int): The option used to select an available service [0-4].
    """
    match options:
        case 0:
            port_scanner(args.ip, args.port)
        case 1:
            banner_grabber(args.ip, args.port)
        case 2:
            tcp_client_server(args.ip, args.port)
        case 3:
            udp_client_server(args.ip, args.port)
        case 4:
            chat_client_server(args.ip, args.port)
        case _:
            message_func.invalid_arg()


if len(argv) <= 1:
    message_func.tool_kit()

parser = ArgumentParser(description="A simple Socket Programming Toolkit.")
parser.add_argument(
    "options",
    type=int,
    help="Used for selecting tools from [0-4].",
)
parser.add_argument(
    "ip",
    help="Used to specify IPv4 address.",
)
parser.add_argument(
    "-p",
    "--port",
    help="Used to specify Port number.",
)
parser.add_argument(
    "-F",
    "--Fast",
    help="Scan 100 most common ports, instead of all.",
    action="store_true",
)
args = parser.parse_args()
options = args.options

if port_func.check_ip_address(args.ip):
    distributing_function(options)
else:
    message_func.invalid_ip()
