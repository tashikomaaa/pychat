#!/usr/bin/env python3

from socket import *
from threading import Thread
import fcntl, os

def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        oldflags = fcntl.fcntl(client, fcntl.F_GETFL)
        fcntl.fcntl(client, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
        print("%s:%s has connected." % client_address)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    name = None
    while True:
        try:
            name = client.recv(BUFSIZ).decode("utf-8")
            break
        except :
            pass
    
    welcome = "Welcome %s!" % name
    client.send(bytes(welcome, "utf-8"))
    msg = "%s has joined the chat " % name
    broadcast(bytes(msg, "utf-8"))
    clients[client] = name
    while True:
        print(client)
        msg = None
        while True:
            try:
                msg = client.recv(BUFSIZ)
                break
            except:
                pass
        if msg != bytes("{quit}", "utf-8"):
            broadcast(msg, name+": ")
            client.send(bytes("", "utf-8"))
        else:
            client.send(bytes("{quit}", "utf-8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat" % name, "utf-8"))
            break

def broadcast(msg, prefix=""): 
    print(prefix)
    for sock in clients.keys():
        sock.send(bytes(prefix, "utf-8")+msg)


clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
SERVER.bind(ADDR)


if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
