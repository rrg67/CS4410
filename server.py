#!/usr/bin/python

import getopt
import socket
import sys
import time

# STOP!  Don't change this.  If you do, we will not be able to contact your
# server when grading.  Instead, you should provide command-line arguments to
# this program to select the IP and port on which you want to listen.  See below
# for more details.
host = "127.0.0.1"
port = 8765

def checkNonWhiteSpace(string):
    i = -1
    while (i < len(string)):
        if (string[i] != " "):
           break
        i += 1
    return i

def checkWhiteSpace(string):
    i = -1
    while (i < len(string)):
        if (string[i] == " "):
            break
        i += 1
    return i

def findEndChar(string):
    i = -1
    while (i < len(string)):
        if (string[i:i+6] == "\r\n.\r\n"):
            break
        i += 1
    return i+6

# handle a single client request
class ConnectionHandler:
    def __init__(self, socket):
        self.socket = socket
        self.state = None
        self.completeMessage = None
        self.partialMessage = None
        #self.endMessage = False
        #self.error = False

    def handle(self):
        # Lets the client know a connection has been made
        self.completeMessage = repr(self.socket.recv(1024))
        #print(self.completeMessage)
        while (True):
            if (self.state == None):
                self.socket.send(b"220 rrg67 SMTP CS4410MP3\r\n")
                self.state = "Open"
                print(self.completeMessage)
            self.socket.settimeout(10)
            # Waiting for a HELO command
            elif (self.state == "Open"):
                print("Yes, it is an open state")
                if (self.completeMessage[0:4] == "HELO"):
                    print("made it through HELO if")
                    m = checkNonWhiteSpace(self.completeMessage[5:])
                    if (self.completeMessage[5] != " " and self.completeMessage[5:7] != "\r\n"):
                            self.socket.send(b"500 Error: command not recognized\r\n")
                    elif (self.completeMessage[5] != " "):
                        self.socket.send(b"501 Syntax:  proper syntax\r\n")
                    elif (self.completeMessage[m:m+2] == "\r\n"):
                        self.socket.send(b"501 Syntax:  proper syntax\r\n")
                    else :
                        self.state = "HELO"
                        self.socket.send(b"250 rrg67\r\n")
                        self.state = None
                        self.completeMessage = None
                        #self.partialMessage = None
                        #self.endMessage = False
                else:
                    print("Never made it to the open state")
                    self.socket.send(b"503 Error: need HELO command\r\n")
            # Waiting for a MAIL FROM command
            elif (self.state == "HELO"):
                print ("state is HELO, looking for a MAIL FROM")
            else:
                print("this is the end")
# the main server loop
def serverloop():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # mark the socket so we can rebind quickly to this port number
    # after the socket is closed
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind the socket to the local loopback IP address and special port
    serversocket.bind((host, port))
    # start listening with a backlog of 5 connections
    serversocket.listen(5)

    while True:
        # accept a connection
        (clientsocket, address) = serversocket.accept()
        ct = ConnectionHandler(clientsocket)
        ct.handle()

# You don't have to change below this line.  You can pass command-line arguments
# -h/--host [IP] -p/--port [PORT] to put your server on a different IP/port.
opts, args = getopt.getopt(sys.argv[1:], 'h:p:', ['host=', 'port='])

for k, v in opts:
    if k in ('-h', '--host'):
        host = v
    if k in ('-p', '--port'):
        port = int(v)

print("Server coming up on %s:%i" % (host, port))
serverloop()
