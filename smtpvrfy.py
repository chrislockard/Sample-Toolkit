#!/usr/bin/python
import socket
import sys

if len(sys.argv) != 3:
        print('Usage: %s <smtpserver> <username>' % sys.argv[0])
        sys.exit(0)

# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect
c = s.connect((sys.argv[1], 25))

# Receive Banner
b = s.recv(1024)
print(b)

# VRFY User
s.send('VRFY ' + sys.argv[2] + '\r\n')
result = s.recv(1024)

print(result)

# Close connection
s.close()
