#! /usr/bin/env python3
import sys,os
sys.path.append("../lib")       # for params
import re, socket, params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

sock, addr = lsock.accept()

print("connection rec'd from", addr)


from framedSock import framedSend, framedReceive

while True:
    payload = framedReceive(sock, debug)
    if debug: print("rec'd: ", payload)
    if not payload:
        break
    #payload += b"!"  make emphatic!
    isAFile = payload.decode().split("$")
    if len(isAFile) > 1:
        fileName = isAFile[1].encode()
    else:
        fileName = payload
    framedSend(sock, fileName, debug)
    if isAFile[0] == "IFL":
        if os.path.isfile("serverFolder/"+fileName.decode()):#check if fileName is in server
            framedSend(sock,b"File already in server" ,debug) # FAS = File Already in Server
        else:
            fileW = open("serverFolder/"+fileName.decode(), "wb")
            while True:
                payload = framedReceive(sock, debug)
                if not payload:
                    break
                fileW.write(payload)
                framedSend(sock, payload, debug)


            
        
