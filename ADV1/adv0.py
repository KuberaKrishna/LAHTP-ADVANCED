from sys import argv
from argparse import ArgumentParser

import portFunc, messageFunc

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

def distributingFunction(options):
    match options:
        case 0:
            portScanner(args.ip, args.p)
        case 1:
            # Banner Grabber
            pass
        case 2:
            # TCP Client and Server
            pass
        case 3:
            # UDP Client and Server
            pass
        case 4:
            # Chat Application
            pass

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