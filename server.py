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
        self.completeMessage = ""
        self.partialMessage = None
        #self.endMessage = False
        #self.error = False

    def handle(self):
        # Lets the client know a connection has been made
        #self.completeMessage = (self.socket.recv(1024))
        if (self.state == None):
            self.socket.send(b"220 rrg67 SMTP CS4410MP3\r\n")
            self.state = "Open"
            print("open")
        while (True):
            i = 0
            print("TRUE")
            self.socket.settimeout(10)
            self.partialMessage = (self.socket.recv(1024))
            while (i < len(self.partialMessage)):
                print("in second while loop")
                if (self.partialMessage[i:i+4] == '\\r\\n'):
                    break
                else: 
                    self.completeMessage = self.completeMessage + self.partialMessage
            print("Partial " + self.partialMessage)
            print("Complete " + self.completeMessage)
            
            
        


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
