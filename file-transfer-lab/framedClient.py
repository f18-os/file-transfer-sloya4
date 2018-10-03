#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    (('put', '--put'), "put", "fileName"),
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

fileName = paramMap["put"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)


print("sending hello world")
framedSend(s, b"hello world", debug)
print("received:", framedReceive(s, debug))

if os.path.isfile(fileName): #Check if file exists
    fileR = open(fileName, "rb")
    fileName = "IFL$"+fileName # IF$ To let the server know it is a file
    framedSend(s, fileName.encode(), debug) #Send file name
    receiveP = framedReceive(s, debug)
    print("received:", receiveP) 
    if receiveP.decode() != "File already in server":
        read = fileR.read(100)
        while read:
            read = read.decode().strip().encode()
            framedSend(s, read, debug)
            print("received:", framedReceive(s, debug))
            read = fileR.read(100)
        fileR.close()
