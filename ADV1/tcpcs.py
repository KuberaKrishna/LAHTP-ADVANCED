from re import search
from socket import SO_REUSEADDR, SOL_SOCKET, socket

# Below modules are created by the author.
import messageFunc
from dec import END, GREEN, LIGHT_WHITE

BUFFER = 2048


# This checks whether a port is valid or not, for listening or connecting
def checkPort(port):
    try:
        port_pattern = r"^(?:6553[0-5]|655[0-2]\d|65[0-4]\d{2}|\
            6[0-4]\d{3}|[1-5]\d{4}|[1-9]\d{0,3}|0)$"
        if search(port_pattern, port):
            return int(port)
        else:
            messageFunc.invalidPort()
            return False
    except TypeError:
        messageFunc.noPortMentioned()


# This function executes the appropriate function based on the user's choice.
def socketConnectionStream(ip, port):
    port = checkPort(port)
    if port is not False:
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


# Server Socket code
def socketServer(host_port):
    try:
        try:
            try:
                with socket() as server_socket:
                    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                    """This will set the socket option,
                    to set at socket level and reuse address."""
                    server_socket.bind(host_port)
                    server_socket.listen()
                    messageFunc.serverListening("TCP", host_port)
                    client_socket, client_address = server_socket.accept()

                with client_socket:
                    print(f"Client connected: \
                        {client_address[0]}:{client_address[1]}\n")
                    client_socket.sendall(f"\nConnected to server on port \
                        {host_port[1]}".encode())
                    while True:
                        data = client_socket.recv(
                            BUFFER
                        )  # can receive data up to 2048 bytes
                        if not data:  # no data === client closed connection
                            break
                        message = data.decode().rstrip()
                        messageFunc.receivedMsg(client_address[0], message)
                    print(f"\nThe client [{client_address[0]}] \
                        has disconnected from the server.")
                    messageFunc.serverShutting("TCP")
            except KeyboardInterrupt:
                messageFunc.serverShutting("TCP")
        except PermissionError:
            messageFunc.registeredPort(host_port[1])
    except OSError:
        messageFunc.serverUsedPort(host_port[1])


# Client socket code
def clientSocket(host_port):
    try:
        try:
            try:
                with socket() as client_socket:
                    client_socket.connect(host_port)
                    srv_msg = client_socket.recv(BUFFER)
                    if srv_msg:
                        print(f"{GREEN}{srv_msg.decode().rstrip()}{END}")
                        while True:
                            data = input(f"{LIGHT_WHITE}\
                            Enter something: {END}")
                            if data.lower() == "/quit"\
                               or data.lower() == "/exit":
                                break
                            client_socket.sendall(data.encode())
            except KeyboardInterrupt:
                messageFunc.clientQuit(host_port)
        except BrokenPipeError:
            messageFunc.serverError()
    except ConnectionRefusedError:
        messageFunc.serverWarning()
