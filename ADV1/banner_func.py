from re import search
from socket import socket

# Below modules are created by the author.
import message_func
from dec import BOLD, END, GREEN, LIGHT_WHITE, YELLOW
from port_func import NOW, check_port, duplicate_port_check

BUFFER = 1024

no_banner_grabbed = 0
banner_grabbed = 0
duplicate_port = 0


def custom_grabber(ip, symb_checking_port):
    """
    Validates the port input and assigns it to the corresponding scan
    based on the value provided by the user.

    Args:
        ip (str): The IPv4 address of the target.
        symb_checking_port (str): Symbols for port validation ("," and "-").
    """
    global duplicate_port
    result = None
    hyphen = "-" in symb_checking_port and symb_checking_port.count("-") == 1
    comma = "," in symb_checking_port
    one_hyphen_check_pattern = r"^-$"

    if search(one_hyphen_check_pattern, symb_checking_port):
        all_banner_grabber(ip)
        return
    if hyphen is True:
        symb_checking_port = symb_checking_port.split("-")
        result = check_port(symb_checking_port)
        if result is True:
            duplicate_no = duplicate_port_check(symb_checking_port)
            if duplicate_no != 0:
                duplicate_port = duplicate_no
            hyphen_grabber(ip, symb_checking_port)
    elif comma is True:
        symb_checking_port = symb_checking_port.split(",")
        result = check_port(symb_checking_port)
        if result is True:
            duplicate_no = duplicate_port_check(symb_checking_port)
            if duplicate_no != 0:
                duplicate_port = duplicate_no
            symb_checking_port = list(dict.fromkeys(symb_checking_port))
            comma_grabber(ip, symb_checking_port)
    elif check_port(symb_checking_port) is True:
        banner_grabber(ip, symb_checking_port)
    else:
        message_func.invalid_port()


def print_header(ip):
    """
    Displays a header message
    """
    print(
        f"\n{GREEN}Starting Banner Grabber at {NOW}{END}\n"
        f"Banner Grabbing report for {ip}\n\n{BOLD}PORT | SERVICE{END}"
    )


def banner_grabber(ip, port_no):
    """
    Main function for grabbing banners from the specified ports.

    Args:
        ip (str): IPv4 address.
        port_no (str): The port or ports to grab banners from.
    """
    global banner_grabbed, no_banner_grabbed
    host_port = (ip, int(port_no))  # will make sure the 'port_no' is int.
    try:
        with socket() as sock:
            sock = socket()
            sock.settimeout(6)
            conn_status = sock.connect_ex(host_port)
            if conn_status == 0:
                banner = sock.recv(BUFFER)
                if banner:
                    banner_grabbed += 1
                    banner = banner.decode("UTF-8").strip()
                    print(f"{LIGHT_WHITE}{port_no} | {banner}{END}")
            else:
                no_banner_grabbed += 1
    except TimeoutError:
        print(
            f"{YELLOW}Couldn't find any banner from the port: {port_no}{END}"
        )


def all_banner_grabber(ip):
    """
    Main function for grabbing banners from all ports.

    Args:
        ip (str): The IPv4 address of the target.
    """
    try:
        for ports in range(65536):
            banner_grabber(ip, ports)
    except KeyboardInterrupt:
        message_func.toolkit_aborted()


def hyphen_grabber(ip, port_no):
    """
    Used when the user enters a hyphen (-) between port numbers.

    Args:
        ip (str): The IPv4 address of the target.
        port_no (str): The port range to grab banners from.
    """
    try:
        port_start, port_end = int(port_no[0]), int(port_no[1])
        if port_start <= port_end:
            for ports in range(port_start, port_end + 1):
                banner_grabber(ip, ports)
        else:
            message_func.port_greater(port_start, port_end)
    except KeyboardInterrupt:
        message_func.toolkit_aborted()


def comma_grabber(ip, port_no):
    """
    Used when the user enters a comma (,) between port numbers.

    Args:
        ip (str): The IPv4 address of the target.
        port_no (str): The port range to grab banners from.
    """

    try:
        port_len = len(port_no)
        for i in range(port_len):
            banner_grabber(ip, port_no[i])
    except KeyboardInterrupt:
        message_func.toolkit_aborted()


def print_end():
    """
    Displays a conclusion message
    """
    end_msg = (
        f"\nBanner Grabbing done: Banner Grabbed: {banner_grabbed},"
        f"Closed ports: {no_banner_grabbed}"
    )
    dup_msg = f"Duplicate ports: {duplicate_port}\n"
    if duplicate_port != 0:
        print(end_msg + dup_msg)
    else:
        print(end_msg, end="\n\n")
