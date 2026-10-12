from pyfiglet import figlet_format

from dec import RED, LIGHT_RED, LIGHT_YELLOW, BOLD, BLINK, END
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

def unwantedOpt():
    print('*-'*27, end="*\n")
    print(f"\n\t{LIGHT_YELLOW}Unwanted options were specified ['-F'].{END}\n")
    print('*-'*27, end="*\n\n")

## Port Message
def invalidPort():
    print()
    print('x-'*35, end="x\n")
    print(f"\n\t{RED}Ports specified must be between 0 and 65535 inclusive\n\t\t\t{BLINK}QUITTING!{END}\n")
    print('x-'*35, end="x\n\n")

def portGreater(s_port, e_port):
    print('x-'*27, end="x\n")
    print(f"\n\t{LIGHT_RED}[{s_port}] is greater than [{e_port}]{END}\n")
    print('x-'*27, end="x\n\n")

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