#!/usr/bin/python
import socket
import sys

def connect(ip_addr,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip_addr,port))
    s.send("Hello!\n")
    s.close()

if len(sys.argv) != 3:
    print "Usage: %s <ip_addr> <port>" % sys.argv[0]
    sys.exit(0)
else:
    connect(sys.argv[1], int(sys.argv[2]))

