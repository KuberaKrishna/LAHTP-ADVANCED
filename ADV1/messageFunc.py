from pyfiglet import figlet_format

from dec import RED, GREEN, YELLOW, LIGHT_RED, LIGHT_BLUE, LIGHT_GREEN, LIGHT_YELLOW, BOLD, BLINK, END
# All these functions are used to avoid repeating the `print` statement multiple times.
## General Message

def welcomeMsg():
        welcome_msg = figlet_format("Python3 Socket Toolkit")
        print("+-"*40,end="+\n")
        print(f"{welcome_msg}")
        print("+-"*40,end="+\n")

def toolKit():
    print(f"\n\n{BOLD}[0] Port Scanner\n[1] Banner Grabber\n[2] TCP Client/Server\n[3] UDP Client/Server\n[4] Chat Application\n\n{END}")

def invalidArg():
    print()
    print("x-"*26, end="x\n")
    print(f"\n\t{RED}Invalid arguement valued passed!{END}\n")
    print("x-"*26, end="x\n\n")

def invalidOpt():
    print()
    print("x-"*24, end="x\n")
    print(f"\n\t{RED}Invalid options valued passed!{END}\n")
    print("x-"*24, end="x\n\n")

def unwantedOpt():
    print('*-'*27, end="*\n")
    print(f"\n\t{LIGHT_YELLOW}Unwanted options were specified ['-F'].{END}\n")
    print('*-'*27, end="*\n\n")

## Port Message
def registeredPort(port_no):
    print()
    print('x-'*35, end="x\n")
    print(f"\n\t{RED}Server didn't start! You mentioned well-known port '{port_no}'\n\t\tthat you don't have permission to use.{END}\n")
    print('x-'*35, end="x\n\n")

def serverUsedPort(port_no):
    print("x-"*30, end="x\n")
    print(f"\n\t{YELLOW}Check whether any other server is running on the\n\t\tsame port you specified: [{port_no}]\n{END}")
    print("x-"*30, end="x\n\n")

def invalidPort():
    print()
    print('x-'*35, end="x\n")
    print(f"\n\t{RED}Ports specified must be between 0 and 65535 inclusive\n\t\t\t{BLINK}QUITTING!{END}\n")
    print('x-'*35, end="x\n\n")

def portGreater(s_port, e_port):
    print('x-'*27, end="x\n")
    print(f"\n\t{LIGHT_RED}[{s_port}] is greater than [{e_port}]{END}\n")
    print('x-'*27, end="x\n\n")

def noPortMentioned():
    print()
    print('x-'*25, end="x\n")
    print(f"\n\t{RED}Check whether a port is mentioned.{END}\n")
    print('x-'*25, end="x\n\n")

def toolKitAborted():
    print()
    print('x-'*17, end="x\n")
    print(f'\n\t{RED}Toolkit {BLINK}aborted!!{END}\n')
    print('x-'*17, end="x\n\n")

## IP Message
def invalidIP():
    print()
    print('x-'*32, end="x\n")
    print(f"\n\t{RED}IPv4 address specified must be between 0 and 255,\n\t\tshould only be numbers.\n\t\t\t{BLINK}QUITTING!{END}\n")
    print('x-'*32, end="x\n\n")

def serviceList():
    print(f"\n{BOLD}[1]Server Listening\n[2]Client Connecting{END}\n")

## Server Message

def serverInit(name):
    print()
    print('#-'*27, end="#\n")
    print(f"\n\t{name} server initiated ...\n")
    print('#-'*27, end="#\n")

def serverListening(name, host_port):
    print(f"\n{GREEN}{name} Server Started Listening on {host_port[0]} {host_port[1]}{END}")

def receivedMsg(client_address, message):
    print(f"Received from [{client_address}]: {message}")

def serverWarning():
    print('*-'*27, end="*\n")
    print(f"\n\t{YELLOW}Check whether the server is running.{END}\n")
    print('*-'*27, end="*\n\n")

def serverError():
    print("x-"*30, end="x\n")
    print(f"\n\t{RED}500 Internal Server Error{END}\n")
    print(f"{YELLOW}[Error brief]: The server may be offline or unavailable.{END}")
    print("x-"*30, end="x\n\n")

def serverShutting(name):
    print()
    print('x-'*27, end="x\n")
    print(f"\n\t{LIGHT_GREEN}{name} server shutting down ...{END}\n")
    print('x-'*27, end="x\n\n")

## Client Message
def clientQuit(host_port):
    print()
    print('x-'*27, end="x\n")
    print(f'\n\t{LIGHT_BLUE}You quited from the server {host_port[0]}:{host_port[1]}{END}\n')
    print('x-'*27, end="x\n\n")