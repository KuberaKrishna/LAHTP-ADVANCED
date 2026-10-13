# PRESENTING MY LAHTP ADVANCED ASSIGNMENT - 1 SOCKET PROGRAMMING TOOLKIT

## Introduction
* Developed a lightweight socket programming toolkit in Python3 for Assignment 1 of the LAHTP Advanced course under SNA, implementing the following functions:
    * [0] Port Scanner
    * [1] Banner Grabber
    * [2] TCP Client/Server
    * [3] UDP Client/Server
    * [4] Chat Application(Multi-threaded)
## ⚠️ Disclaimer
* This toolkit is intended for educational purposes only. Do not use it against systems you do not own or have explicit permission to test.(If you do, your activity may be recorded in their logs).

## ⚙️ Before that ...
* You need to install `csv` module.
* To install a module, use: `pip3 install <module_name>`.


# Instructions
* `How does this tool work?`: You need to mention the necessary arguments, options, or flags required to use the tool.
* `Read all the instructions carefully to use the toolkit effectively.`
### General Command Usage
Example Command| Purpose
-|-
python3 <program_name.py> | List all the availale tools.
python3 <program_name.py> --help | Shows available arguments and options to use.

## [0] Port Scanner
* This is scan is noisy, supports only TCP connect scans, which works by completing the TCP 3-way handshake.
* This will by default try to connect all the ports, if `-p` or `--port` and `-F` or `--Fast` flag is not mentioned.
* Service names are identified using a CSV file containing the 100 most common port numbers, their corresponding services, and their protocols for better understanding.
* We can also use `-F` or `--Fast` to enable fast mode and decrease the number of scanned ports from all ports to 100 most common ports.
* `-p22` or `--port 22` and `-F` or `--Fast` are two different scan options; use them separately to avoid conflicts.
* Duplicate ports are ignored.

### Usage
Example Command | Purpose
-|-
python3 <program_name.py> 0 IP or python3 <program_name.py> 0 IP -p-| It scans all the ports.
python3 <program_name.py> 0 IP -F | It scans 100 most common ports.
python3 <program_name.py> 0 IP -p22| It scans only a single port.
python3 <program_name.py> 0 IP -p5000,22,5432| It scans only the given list of port.
python3 <program_name.py> 0 IP -p1-1025 | It scans only the specified range of ports.

## [1] Banner Grabber
* This tool connects to a network service and retrieves its banner or response to identify the service and software running on a port, and sometimes its version.
* Some require a specific request or protocol handshake, while others hide or omit identifying information.
* `Couldn't find any banner from the port: <port_no>`: This error occurs when the connected port fails to respond within the specified time limit (timeout error).
* By default, the program attempts to grab banners from all ports if the `-p`or `--port` option or flag is not specified.
* You may also get an empty string or non-printable characters. To inspect them, use Python’s `repr()` function, which returns an official string representation of an object. For example, you might see something like `'\x01\x00\x00\x00'`, which is a Python-style representation of a string containing escaped characters.
* `-p22` or `--port 22` and `-F` or `--Fast` are two different scan options; use them separately to avoid conflicts.
* Duplicate ports are ignored.

### Usage
Example Command | Purpose
-|-
python3 <program_name.py> 1 IP or python3 <program_name.py> 1 IP -p-| It connects all the port and retrieve banner(if available)
python3 <program_name.py> 1 IP -p 80| It grabs the banner from a single port.
python3 <program_name.py> 1 IP -p 143,179,110| It grabs the banner from the given list of port.
python3 <program_name.py> 1 IP -p 443-65436 | It grabs the banner from the specified range of ports.

## [2] TCP Client/Server
* TCP is connection-oriented: it sets up a connection first and ensures data arrives reliably and in order.
* A simple TCP client-server program where the server receives and prints messages sent by the client.
* Only one client can communicate with the server at a time.
* Client can type `'/exit'` or `'/quit'` to leave the server.

### Usage
Example Command | Purpose
-|-
python3 <program_name.py> 2 IP --port 6789| This prompts the user to choose whether to start the client or server on the specified port.

## [3] UDP Client/Server
* UDP is connectionless: no handshake, no delivery guarantee. 
* A simple UDP client-server program in which the server receives and prints messages sent by the client.
* Only one client can communicate with the server at a time, and communication is possible even when no server is running(in which case the data is simply lost).
* Client can type `'/exit'` or `'/quit'` to leave the server.

### Usage
Example Command | Purpose
-|-
python3 <program_name.py> 3 IP --port 6556| This prompts the user to choose whether to start the client or server on the specified port.

### [4] Chat Application(Multi-threaded)
* Created a simple chat application(TCP, obviously) using socket programming and multithreading.
* Multiple users can communicate with other connected clients. Users can set a nickname to be identified by others or type `'/skip'` to remain anonymous. Other users in the chat will see them as `(Anonymous)`.
* If you don't see any prompt, press Enter.
* Connected clients can see which users have joined or left the server. The server also maintains a log of these events, but the logs are not stored permanently.
* Clients can type `'/exit'` or `'/quit'` to leave the chat.

#### Usage
Example Command | Purpose
-|-
python3 <program_name.py> 4 IP -p8888| This prompts the user to choose whether to start the client or server on the specified port.