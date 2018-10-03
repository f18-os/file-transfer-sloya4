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


from framedSock import framedSend, framedReceive

while True: # keeps the server open
    sock, addr = lsock.accept() # waits for a client 
    print("connection rec'd from", addr)            

    if not os.fork(): # os.fork() = 0 if child is created
        while True: # while the client keeps sending messages
            payload = framedReceive(sock, debug)
            if debug: print("rec'd: ", payload) # to check is getting the message
            if not payload: # if empty, stop
                break
            #payload += b"!"  make emphatic!
            isAFile = payload.decode().split("$")
            if len(isAFile) > 1: # if it has a file name
                fileName = isAFile[1].encode()
            else:
                fileName = payload
            framedSend(sock, fileName, debug)
            if isAFile[0] == "IFL":
                if os.path.isfile("serverFolder/"+fileName.decode()):#check if fileName is in server
                    framedSend(sock,b"File already in server" ,debug) # File Already in Server
                else:
                    fileW = open("serverFolder/"+fileName.decode(), "wb")
                    while True:
                        payload = framedReceive(sock, debug)
                        if not payload:
                            break
                        fileW.write(payload)
                        framedSend(sock, payload, debug)
                    fileW.close()

            
        
