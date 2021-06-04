#!/usr/bin/python

import socket, sys
import threading
import json
import time

def notifyClientAboutConnection(clientName, targetName, clientsocket):
    print("Notify client " + targetName + " about connection")
    targetListener = listeners[targetName]
    targetListener.send(b"Ask for connection by: " + clientName.encode('utf-8'))
    res1 = targetListener.recv(512).decode("utf-8")

    if not res1 == "OK":
        clientsocket.send(b"NO")
        print("Client " + targetName + " declined request from " + clientName)
        return False

    targetListener.send(b"Connection adress: " + str(json.dumps(requests[targetName])).encode('utf-8'))
    res2 = targetListener.recv(512).decode("utf-8")
    if res2 == "OK":
        targetSocket = sockets[targetName]
        targetSocket.close()
        sockets.pop(targetName)
        targetListener.close()
        listeners.pop(targetName)
        requests.pop(targetName)
        clients.pop(targetName)
        print("Clients: " + clientName + " and " + targetName + " go chating")
        clientsocket.send(b"OK")
        return True


def handle_client(clientsocket, clientaddress):
    print(b"Received the connection from: " + str(clientaddress).encode('utf-8'))
    rawName = clientsocket.recv(512).decode("utf-8") 
    clientName = rawName[len("My name is "):]
    clientsocket.send(b"OK")

    status = clientsocket.recv(512).decode("utf-8") 
    if status == "I am listener":
        listeners[clientName] = clientsocket
        clientsocket.send(b"OK")
        return

    clients[clientName] = clientaddress
    sockets[clientName] = clientsocket
    clientsocket.send(b"OK")

    while clientName in clients:
        try:
            time.sleep(1)
            query = clientsocket.recv(512).decode("utf-8")

            if query == "Get users":
                jsonClients = json.dumps(clients)
                print("Clients list:\n " + jsonClients)
                clientsocket.send(str(jsonClients).encode('utf-8'))

            elif query[:len("Get user adress: "):] == "Get user adress: ":
                targetName = query[len("Get user adress: "):]
                jsonClients = json.dumps(clients[targetName])
                print("Client " + targetName + " has adress: " + jsonClients)
                clientsocket.send(str(jsonClients).encode('utf-8'))

            elif query[:len("Start listen for: "):] == "Start listen for: ":
                targetName = query[len("Start listen for: "):]
                clientsocket.send(b"OK")
                rawPort = clientsocket.recv(512).decode("utf-8") 
                port = rawPort[len("Start listen on port: "):]
                print("Client " + clientName + " is waiting for " + targetName + " on port " + port)
                requests[targetName] = (clientaddress[0], int(port))
                if notifyClientAboutConnection(clientName, targetName, clientsocket):
                    clientsocket.close()
                    listeners[clientName].close()
                    clients.pop(clientName)
                    sockets.pop(clientName)
                    break

            elif query == "Bye":
                clientsocket.close()
                listeners[clientName].send(str("Exit").encode('utf-8'))
                listeners[clientName].close()
                listeners.pop(clientName)
                clients.pop(clientName)
                sockets.pop(clientName)
                print("Client " + clientName + " quits")
                break
        except:
            break
    return

clients = {}
sockets = {}
requests = {}
listeners = {}

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('localhost',5091))
s.listen(5)
print("Server is running on port 5091:")
while True:
	clientsocket,clientaddress=s.accept()
	t = threading.Thread(target=handle_client, args=(clientsocket,clientaddress,))
	t.start()
