from csv import reader
from datetime import datetime
from re import search
from socket import socket

# Below modules are created by the author.
import message_func
from dec import BOLD, END, GREEN, LIGHT_WHITE

PORTS_100_FILE = (
    "top-100-port.csv"  # This "*.csv" has the Top 100 ports scanned by nmap
)
NOW = datetime.now().strftime("%Y-%m-%d %H:%M")  # The current time

scanned_port = 0
closed_port = 0
duplicate_port = 0

# Checking if IPv4 address and Port number is Valid or Not


def check_ip_address(ip_address):
    """
    Validates the IPv4 address provided by the user.

    Args:
        ip_address: User-Provided IPv4 address.
    """
    ipv4_pattern = r"^(?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})(?:\.(?!$)|$)){4}$"
    if search(ipv4_pattern, ip_address):
        return ip_address
    else:
        return False


def check_port(port_no):
    """
    Validates the port number provided by the user.

    Args:
        port_no (str): User-Provided port number.
    """
    if port_no is None:
        return False
    port_pattern = r"^(?:6553[0-5]|655[0-2]\d|65[0-4]\d{2}|\
        6[0-4]\d{3}|[1-5]\d{4}|[1-9]\d{0,3}|0)$"
    status = None
    if isinstance(port_no, list):
        for ports in port_no:
            if search(port_pattern, ports):
                status = True
            else:
                message_func.invalid_port()
                return False
    elif isinstance(port_no, str) and search(port_pattern, port_no):
        return True
    return status


def custom_scan(ip, symb_checking_port):
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
        all_port(ip)
        return
    if hyphen is True:
        symb_checking_port = symb_checking_port.split("-")
        result = check_port(symb_checking_port)
        if result is True:
            duplicate_no = duplicate_port_check(symb_checking_port)
            if duplicate_no != 0:
                duplicate_port = duplicate_no
            hyphen_scan(ip, symb_checking_port)
    elif comma is True:
        symb_checking_port = symb_checking_port.split(",")
        result = check_port(symb_checking_port)
        if result is True:
            duplicate_no = duplicate_port_check(symb_checking_port)
            if duplicate_no != 0:
                duplicate_port = duplicate_no
            symb_checking_port = list(dict.fromkeys(symb_checking_port))
            comma_scan(ip, symb_checking_port)
    elif check_port(symb_checking_port) is True:
        port_scan(ip, symb_checking_port)
    else:
        message_func.invalid_port()


def duplicate_port_check(port_no):
    """
    Checks whether the user has specified a duplicate port number.

    Args:
        port_no (int): Port number specified by the user.
    """
    d_port = 0
    seen = set()
    duplicate = set()
    for port in port_no:
        if port in seen:
            duplicate.add(port)
            d_port += 1
        else:
            seen.add(port)
    return d_port


# Port Scanning Function


def port_scan(ip, port_no):
    """
    Main function for port scanning.

    Args:
        ip (str): The IPv4 address of the target.
        port_no (int): The port or ports to scan.
    """
    global scanned_port, closed_port
    port_no = int(port_no)  # make sure the port is int
    host_port = (ip, port_no)
    with socket() as sock:
        sock = socket()
        sock.settimeout(2)
        status = sock.connect_ex(host_port)
        if status == 0:
            scanned_port += 1
            print_result(port_no)
        else:
            closed_port += 1


def fast_mode(ip):
    """
    Scans the 100 most common ports.

    Args:
        ip (str): The IPv4 address of the target.
    """
    with open(PORTS_100_FILE, newline="") as csvfile:
        port_svc_file = reader(csvfile)
        for port in port_svc_file:
            port_scan(ip, port[0])


def all_port(ip):
    """
    Scans all the most ports [0-65535].

    Args:
        ip (str): The IPv4 address of the target.
    """
    try:
        for ports in range(65536):
            port_scan(ip, ports)
    except KeyboardInterrupt:
        message_func.toolkit_aborted()


def hyphen_scan(ip, port_no):
    """"
    Used when the user enters a hyphen (-) between port numbers.

    Args:
        ip (str): The IPv4 address of the target.
        port_no (str): The port range to scan from.
    """
    try:
        port_start, port_end = int(port_no[0]), int(port_no[1])
        if port_start <= port_end:
            for port in range(port_start, port_end + 1):
                port_scan(ip, port)
        else:
            message_func.port_greater(port_start, port_end)
    except KeyboardInterrupt:
        message_func.toolkit_aborted()


def comma_scan(ip, port_no):
    """
    Used when the user enters a comma (,) between port numbers.

    Args:
        ip (str): The IPv4 address of the target.
        port_no (str): The port range to scan from.
    """
    try:
        port_len = len(port_no)
        for i in range(port_len):
            port_scan(ip, port_no[i])
    except KeyboardInterrupt:
        message_func.toolkit_aborted()


def print_header(ip):
    """
    Displays a header message

    Args:
        ip (str): The IPv4 address of the target.
    """
    print(
        f"\n{GREEN}Starting Port Scanner at {NOW}{END}\n"
        f"Port Scan report for {ip}\n"
        f"{BOLD}\nPORT | STATE | SERVICE{END}"
    )


def known_100_ports(port_no):
    """
    This will read the 100 most common ports from a top-100-port.csv file.
    The user can identify known banners associated with commonly used ports.

    Args:
        port_no (str): The port or ports are scanned.
    """
    with open(PORTS_100_FILE, newline="") as csvfile:
        port = reader(csvfile)
        for row in port:
            if port_no == int(row[0]):
                return row


def print_result(port_no):
    """
    This will print the port scan results and
    maps it's banner name from the top-100-port.csv file.

    Args:
        port_no (str): The port range to grab banners from.
    """
    row = known_100_ports(port_no)
    if row is not None:
        print(f"{LIGHT_WHITE}{port_no}/{row[1]} | open | {row[2]}{END}")
    elif row is None:
        print(f"{LIGHT_WHITE}{port_no}  | open | unknown{END}")


def print_end():
    """
    Displays a conclusion message.
    """
    end_msg = (
        f"\nPort Scan done: Scanned ports: {scanned_port},"
        f" Closed ports: {closed_port}"
    )
    dup_msg = f"Duplicate ports: {duplicate_port}\n"
    if duplicate_port != 0:
        print(end_msg + dup_msg)
    else:
        print(end_msg, end="\n\n")
