from re import search
from socket import socket
from csv import reader
from datetime import datetime

# Below modules are created by the author.
from dec import GREEN, LIGHT_WHITE, BOLD, END
import messageFunc

PORTS_100_FILE = "top-100-port.csv" # This "*.csv" has the Top 100 ports scanned by nmap
NOW = datetime.now().strftime("%Y-%m-%d %H:%M") # The current time

scanned_port = 0
closed_port = 0
duplicate_port = 0

# Checking if IPv4 address and Port number is Valid or Not

## Validating the IPv4 address, retrieved from the user.
def checkIpAddress(ip_address):
    ipv4_pattern = r"^(?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})(?:\.(?!$)|$)){4}$"
    if search(ipv4_pattern, ip_address):
        return ip_address
    else:
        return False

## Validating the port retrieved from the user.
def checkPort(port_num):
    if port_num == None:
        return False
    port_pattern = r"^(?:6553[0-5]|655[0-2]\d|65[0-4]\d{2}|6[0-4]\d{3}|[1-5]\d{4}|[1-9]\d{0,3}|0)$"
    status = None
    if isinstance(port_num, list):
        for ports in port_num:
            if search(port_pattern, ports):
                status = True
            else:
                messageFunc.invalidPort()
                return False
    elif isinstance(port_num, str):
        if search(port_pattern, port_num):
            return True
    return status
 
## This will verify the port and distribute it to the respective scan.
def customScan(ip, symb_checking_port):
    global duplicate_port
    result=None
    hyphen = "-" in symb_checking_port and symb_checking_port.count("-") == 1
    comma = "," in symb_checking_port
    one_hyphen_check_pattern = r"^-$"
    if search(one_hyphen_check_pattern, symb_checking_port):
        allPort(ip)
        return
    if hyphen == True:
        symb_checking_port = symb_checking_port.split('-')
        result=checkPort(symb_checking_port)
        if result == True:
            duplicate_no = duplicatePortCheck(symb_checking_port)
            if duplicate_no != 0:
                duplicate_port = duplicate_no
            hyphenScan(ip, symb_checking_port)
    elif comma == True:
        symb_checking_port = symb_checking_port.split(",")
        result=checkPort(symb_checking_port)
        if result == True:
            duplicate_no = duplicatePortCheck(symb_checking_port)
            if duplicate_no != 0:
                duplicate_port = duplicate_no
            symb_checking_port = list(dict.fromkeys(symb_checking_port))
            commaScan(ip, symb_checking_port)
    elif checkPort(symb_checking_port) == True:
        portScan(ip, symb_checking_port)
    else:
        messageFunc.invalidPort()

## Checks whether the user has specified a duplicate port number.
def duplicatePortCheck(ports):
    d_port = 0
    seen = set()
    duplicate = set()
    for port in ports:
        if port in seen:
            duplicate.add(port)
            d_port+=1
        else:
            seen.add(port)
    return d_port

# Port Scanning Function

## Main Port Scanning ().
def portScan(ip, port):
    global scanned_port, closed_port
    port = int(port) # This will ensure that all the port parameter is a number and not a string.
    host_port = (ip, port)
    with socket() as sock:
        sock = socket()
        sock.settimeout(2)
        status = sock.connect_ex(host_port)
        if status == 0:
            scanned_port+=1
            printResult(port)
        else:
            closed_port+=1

## This scan will scan the 100 most common port.
def fastMode(ip):
    with open(PORTS_100_FILE, newline='') as csvfile:
        file = reader(csvfile)
        for port in file:
            portScan(ip, port[0])

## This scan will try to connect all the available ports.
def allPort(ip):
    try:
        for ports in range(0, 65536):
            portScan(ip, ports)
    except KeyboardInterrupt:
        messageFunc.toolKitAborted()

## This scan is for hyphen seperated ports.
def hyphenScan(ip, ports):
    try:
        port_start, port_end = int(ports[0]), int(ports[1])
        if port_start <= port_end:
            for port in range(port_start, port_end + 1):
                portScan(ip, port)
        else:
            messageFunc.portGreater(port_start, port_end)
    except KeyboardInterrupt:
        messageFunc.toolKitAborted()

## This scan is for comma seperated ports.
def commaScan(ip, port):
    try:
        port_len = len(port)
        for i in range(0, port_len):
            portScan(ip, port[i])
    except KeyboardInterrupt:
        messageFunc.toolKitAborted()


## Like a header or a starting message.
def printHeader(ip):
    print(f"\n{GREEN}Starting Port Scanner at {NOW}{END}\nPort Scan report for {ip}\n{BOLD}\nPORT | STATE |  SERVICE{END}")

## This will read a 100 known ports from a "top-100-port.csv" file,
##  for printResult(), so that user know some known banner from the common most port.
def known100ports(port_no):
    with open(PORTS_100_FILE, newline='') as csvfile:
        port = reader(csvfile)
        for row in port:
            if port_no == int(row[0]):
                return row

## This will print the port scan results and maps it's banner name from "top-100-port.csv" file.
def printResult(ports):
    row = known100ports(ports)
    if row != None:
        print(f"{LIGHT_WHITE}{row[0]}/{row[1]} | open | {row[2]}{END}")
    elif row == None:
        print(f"{LIGHT_WHITE}{ports}  | open | unknown{END}")

## Like a footer or a conclusion message.
def printEnd():
    global duplicate_port
    end_msg=f"\nPort Scan done: Scanned ports: {scanned_port}, Closed ports: {closed_port} "
    dup_msg=f"Duplicate ports: {duplicate_port}\n"
    if duplicate_port != 0:
        print(end_msg+dup_msg)
    else:
        print(end_msg,end="\n\n")