from re import search
from socket import socket

# Below modules are created by the author.
import messageFunc
from dec import BOLD, END, GREEN, LIGHT_WHITE, YELLOW
from portFunc import NOW, checkPort, duplicatePortCheck

BUFFER = 1024

no_banner_grabbed = 0
banner_grabbed = 0
duplicate_port = 0


# Validating the port retrieved from the user.


# This will verify the port and assign it to the respective scan,
# based on the value provided by the user.
def customGrabber(ip, symb_checking_port):
    global duplicate_port
    result = None
    hyphen = "-" in symb_checking_port and symb_checking_port.count("-") == 1
    comma = "," in symb_checking_port
    one_hyphen_check_pattern = r"^-$"
    if search(one_hyphen_check_pattern, symb_checking_port):
        allBannerGrabber(ip)
        return
    if hyphen is True:
        symb_checking_port = symb_checking_port.split("-")
        result = checkPort(symb_checking_port)
        if result is True:
            duplicate_no = duplicatePortCheck(symb_checking_port)
            if duplicate_no != 0:
                duplicate_port = duplicate_no
            hyphenGrabber(ip, symb_checking_port)
    elif comma is True:
        symb_checking_port = symb_checking_port.split(",")
        result = checkPort(symb_checking_port)
        if result is True:
            duplicate_no = duplicatePortCheck(symb_checking_port)
            if duplicate_no != 0:
                duplicate_port = duplicate_no
            symb_checking_port = list(dict.fromkeys(symb_checking_port))
            commaGrabber(ip, symb_checking_port)
    elif checkPort(symb_checking_port) is True:
        bannerGrabber(ip, symb_checking_port)
    else:
        messageFunc.invalidPort()


# Banner Grabbing


# Like a header or starting message.
def printHeader(ip):
    print(f"\n{GREEN}Starting Banner Grabber at {NOW}{END}\n\
        Banner Grabbing report for {ip}\n\n{BOLD}PORT | SERVICE{END}")


# Main Banner Grabbing ().
def bannerGrabber(ip, port):
    global banner_grabbed, no_banner_grabbed
    host_port = (ip, int(port))
    # above will make sure it is int
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
                    print(f"{LIGHT_WHITE}{port} | {banner}{END}")
            else:
                no_banner_grabbed += 1
    except TimeoutError:
        print(f"{YELLOW}Couldn't find any banner from the port: {port}{END}")


# This function is used when, user type "-p-".
def allBannerGrabber(ip):
    try:
        for ports in range(65536):
            bannerGrabber(ip, ports)
    except KeyboardInterrupt:
        messageFunc.toolKitAborted()


# This function is used when user type hyphen(-) in between port numbers.
def hyphenGrabber(ip, port):
    try:
        port_start, port_end = int(port[0]), int(port[1])
        if port_start <= port_end:
            for ports in range(port_start, port_end + 1):
                bannerGrabber(ip, ports)
        else:
            messageFunc.portGreater(port_start, port_end)
    except KeyboardInterrupt:
        messageFunc.toolKitAborted()


# This function is used when, user type comma(,) in between port numbers.
def commaGrabber(ip, port):
    try:
        port_len = len(port)
        for i in range(port_len):
            bannerGrabber(ip, port[i])
    except KeyboardInterrupt:
        messageFunc.toolKitAborted()


# Like a footer or conclusion message.
def printEnd():
    end_msg = f"\nBanner Grabbing done: Banner Grabbed: {banner_grabbed},\
        Closed ports: {no_banner_grabbed} "
    dup_msg = f"Duplicate ports: {duplicate_port}\n"
    if duplicate_port != 0:
        print(end_msg + dup_msg)
    else:
        print(end_msg, end="\n\n")
