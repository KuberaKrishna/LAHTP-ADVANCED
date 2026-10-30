from argparse import ArgumentParser
from sys import argv

# Below modules are created by the author.
import bannerFunc
import chatcs
import messageFunc
import portFunc
import tcpcs
import udpcs

messageFunc.welcomeMsg()


def portScanner(ip, port):
    if args.Fast and args.port:
        messageFunc.unwantedOpt()
    else:
        portFunc.printHeader(ip)
        if not args.port and not args.Fast:
            portFunc.allPort(ip)
        elif args.Fast and not args.port:
            portFunc.fastMode(ip)
        else:
            portFunc.customScan(ip, port)
        portFunc.printEnd()


def bannerGrabber(ip, port):
    if not args.port and not args.Fast:
        bannerFunc.printHeader(ip)
        bannerFunc.allBannerGrabber(ip)
        bannerFunc.printEnd()
    elif not args.Fast:
        bannerFunc.printHeader(ip)
        bannerFunc.customGrabber(ip, port)
        bannerFunc.printEnd()
    else:
        messageFunc.unwantedOpt()


def tcpClientAndServer(ip, port):
    if tcpcs.checkPort(port):
        messageFunc.serverInit("TCP")
        tcpcs.socketConnectionStream(ip, port)


def udpClientAndServer(ip, port):
    if tcpcs.checkPort(port):
        messageFunc.serverInit("UDP")
        udpcs.socketConnectionGram(ip, port)


def chatClientAndServer(ip, port):
    if tcpcs.checkPort(port):
        messageFunc.serverInit("Multi Client Chat")
        chatcs.ChatServerAndClient(ip, port)


def distributingFunction(options):
    match options:
        case 0:
            portScanner(args.ip, args.port)
        case 1:
            bannerGrabber(args.ip, args.port)
        case 2:
            tcpClientAndServer(args.ip, args.port)
        case 3:
            udpClientAndServer(args.ip, args.port)
        case 4:
            chatClientAndServer(args.ip, args.port)
        case _:
            messageFunc.invalidArg()


if len(argv) <= 1:
    messageFunc.toolKit()

parser = ArgumentParser(description="A simple Socket Programming Toolkit.")
parser.add_argument(
    "options",
    type=int,
    help="Used for selecting tools from [0-4].",
)
parser.add_argument(
    "ip",
    help="Used to specify IPv4 Address.",
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

if portFunc.checkIpAddress(args.ip):
    distributingFunction(options)
else:
    messageFunc.invalidIP()
