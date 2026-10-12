from sys import argv
from argparse import ArgumentParser

import portFunc, bannerFunc, tcpcs, udpcs, chatcs, messageFunc

messageFunc.welcomeMsg()

def portScanner(ip, port):
    if args.F and args.p:
        messageFunc.unwantedOpt()
    else:
        portFunc.printHeader(ip)
        if not args.p and not args.F:
            portFunc.allPort(ip)
        elif args.F and not args.p:
            portFunc.fastMode(ip)
        else:
            portFunc.customScan(ip, port)
        portFunc.printEnd()

def bannerGrabber (ip, port):
    if not args.p and not args.F:
        bannerFunc.printHeader(ip)
        bannerFunc.allBannerGrabber(ip)
        bannerFunc.printEnd()
    elif not args.F:
        bannerFunc.printHeader(ip)
        bannerFunc.customGrabber(ip, port)
        bannerFunc.printEnd()
    else:
        messageFunc.unwantedOpt()

def tcpClientAndServer(ip, port):
    if tcpcs.checkPort(port):
        messageFunc.serverInit('TCP')
        tcpcs.socketConnectionStream(ip, port)

def udpClientAndServer(ip, port):
    if tcpcs.checkPort(port):
        messageFunc.serverInit('UDP')
        udpcs.socketConnectionGram(ip, port)

def chatClientAndServer(ip, port):
    if tcpcs.checkPort(port):
        messageFunc.serverInit('Multi Client Chat')
        chatcs.ChatServerAndClient(ip, port)

def distributingFunction(options):
    match options:
        case 0:
            portScanner(args.ip, args.p)
        case 1:
            bannerGrabber(args.ip, args.p)
        case 2:
            tcpClientAndServer(args.ip, args.p)
        case 3:
            udpClientAndServer(args.ip, args.p)
        case 4:
            chatClientAndServer(args.ip, args.p)

if len(argv) <= 1:
    messageFunc.toolKit()

parser = ArgumentParser()
parser.add_argument("o", type=int, help="Used for selecting tools from [0-4]")
parser.add_argument("ip", help="Used to specify IPv4 Address")
parser.add_argument("-p", help="Used to specify Port number")
parser.add_argument("-F", help="Scan 100 most common ports, instead of all", action="store_true")
args = parser.parse_args()
options = args.o

if options <= 4 and options >= 0:
    if portFunc.checkIpAddress(args.ip):
        distributingFunction(options)
    else:
        messageFunc.invalidIP()
else:
    messageFunc.invalidArg()