from socket import socket, AF_INET, SOCK_DGRAM

# Below modules are created by the author.
from tcpcs import checkPort
from dec import LIGHT_WHITE, END
import messageFunc

BUFFER=2048

## This function executes the appropriate function based on the user's choice.
def socketConnectionGram(ip, port):
    port = checkPort(port)
    if port != False:
        global host_port
        host_port = (ip, port)
        messageFunc.serviceList()
        try:
            try:
                try:
                    options = int(input(">> "))
                    match options:
                        case 1:
                            socketServer(host_port)
                        case 2:
                            clientSocket(host_port)
                        case _:
                            messageFunc.invalidOpt()
                except EOFError:
                    messageFunc.toolKitAborted()
            except ValueError:
                messageFunc.invalidOpt()
        except KeyboardInterrupt:
            messageFunc.toolKitAborted()
# Socket Code

## Server Socket code
def socketServer(host_port):
    try:
        try:
            try:
                with socket(AF_INET, SOCK_DGRAM) as server_socket:
                    server_socket.bind(host_port)
                    messageFunc.serverListening('UDP', host_port)
                    while True:
                        data, client_address = server_socket.recvfrom(BUFFER)
                        message = data.decode('utf-8').rstrip()
                        messageFunc.receivedMsg(client_address[0], message)
            except KeyboardInterrupt:
                messageFunc.serverShutting("UDP")
        except PermissionError:
            messageFunc.registeredPort(host_port[1])
    except OSError:
        messageFunc.serverUsedPort(host_port[1])

## Client socket code
def clientSocket(host_port):
    print()
    try:
        with socket(AF_INET, SOCK_DGRAM) as client_socket:
            while True:
                data = input(f"{LIGHT_WHITE}Enter something:{END} ")
                if data.lower() == "/quit" or data.lower() == '/exit':
                    break
                client_socket.sendto(data.encode('utf-8'), host_port)
    except KeyboardInterrupt:
        messageFunc.clientQuit(host_port)