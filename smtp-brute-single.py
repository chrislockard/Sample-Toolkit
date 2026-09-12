#!/usr/bin/python

import socket
import sys

if len(sys.argv) != 3:
    print("Usage: " + sys.argv[0] + " <server IP> <userlist>")
    sys.exit(0)

def main():
    # Create a socket
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the Server
    connect=s.connect((sys.argv[1], 25))

    # Receive and print banner
    banner=s.recv(1024)

    # create file handle to userlist and read items in
    f = open(sys.argv[2], 'r')
    lines = f.readlines()

    # loop through names read from file and perform VRFY on them
    for line in lines:
        # Send a VRFY request to the server and print the results
        s.send('VRFY ' + line + '\r\n')
        result=s.recv(1024)
        if "250" in result:
            print(sys.argv[1], '\t' , line, '\t',  result)
        else:
            pass
            #print "User not found"

    # Close the socket
    s.close()

    # close file handle
    f.close()
    sys.exit(0)

if __name__ == '__main__':
    main()
