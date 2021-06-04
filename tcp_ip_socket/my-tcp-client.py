#!/usr/bin/python
#simple tcp echo client

import socket,sys
import time
import threading

def readFoo(clientsocket, friendName):
	while True:
		try:
			data = clientsocket.recv(512).decode("utf-8")
			if data=="Bye!":
				clientsocket.close()
				print(friendName + " quits")
				break
			else:
				print(friendName + ": " + data)
		except:
			break

def writeFoo(clientsocket):
	while True:
		try:
			data = input()
			if data=='q' or data=='Q':
				clientsocket.send(b"Bye!")
				clientsocket.close()
				print("End session")
				break
			else:
				clientsocket.send(data.encode('utf-8'))
		except:
			break

def startChatingAsServer(port, userName):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(('localhost',int(port)))
    s.listen(1)
    clientsocket,clientaddress=s.accept()
    tRead = threading.Thread(target=readFoo, args=(clientsocket,userName,))
    tRead.start()
    tWrite = threading.Thread(target=writeFoo, args=(clientsocket,))
    tWrite.start()

def startChatingAsClient(name, userAddress):
    c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    adress = userAddress[1:-1].split(', ')
    host = socket.gethostbyaddr(adress[0][1:-1])[0]
    c.connect((host,int(adress[1])))
    tRead = threading.Thread(target=readFoo, args=(c,name,))
    tRead.start()
    tWrite = threading.Thread(target=writeFoo, args=(c,))
    tWrite.start()

def waitingForConnection(clientsocket, name):
    globalListener.connect(('localhost', 5091))
    globalListener.send(b"My name is " + name.encode('utf-8'))
    res1 = globalListener.recv(512).decode("utf-8") 
    globalListener.send(b"I am listener")
    res2 = globalListener.recv(512).decode("utf-8") 
    while res1 == "OK" and res2 == "OK":
        try:
            status = globalListener.recv(512).decode("utf-8") 
            if status[:len("Ask for connection by: "):] == "Ask for connection by: ":
                name = status[len("Ask for connection by: "):]

                answer = input("Accept connection from " + name + "? (Preess OK is yes)\n")
                globalListener.send(answer.encode('utf-8'))
                
                if not answer == "OK":
                    continue
                    
                print("Start chat with: " + name)

                rawAdress = globalListener.recv(512).decode("utf-8") 
                adress = rawAdress[len("Connection adress: "):]
                globalListener.send(b"OK")
                
                globalListener.close()
                clientsocket.close()
                startChatingAsClient(name, adress)
                break
            elif status == "Exit":
                break
        except:
            break

globalListener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
c.connect(('localhost', 5091))

name = input("Enter your name:\n")
c.send(b"My name is " + name.encode('utf-8'))
res1 = c.recv(512).decode("utf-8") 
c.send(b"I am client")
res2 = c.recv(512).decode("utf-8") 

t = threading.Thread(target=waitingForConnection, args=(c,name,))
t.start()
while res1 == "OK" and res2 == "OK" and c._closed == False:
    option = input('Choose an option:\n Press U to get users list\n Press A to get user adress\n Press S to start chat\n Press Q to quit\n')

    if option == 'U':
        c.send(b"Get users")
        users = c.recv(512).decode("utf-8") 
        print("Active users list:\n" + users)
    elif option == 'A':
        userName = input("Enter user name:\n")
        c.send(b"Get user adress: " + userName.encode('utf-8'))
        userAddress = c.recv(512).decode("utf-8") 
        print("User " + userName + " has adress: " + userAddress)
    elif option == 'S':
        userName = input("Enter user name:\n")
        listenPort = input("Enter port:\n")
        print("Waiting for " + userName)
        c.send(b"Start listen for: " + userName.encode('utf-8'))
        r = c.recv(512)
        c.send(b"Start listen on port: " + listenPort.encode('utf-8'))
        res = c.recv(512).decode("utf-8")
        if res == "OK":
            c.close()
            globalListener.close()
            print("Start chat with: " + userName)
            startChatingAsServer(listenPort, userName)
        else:
            print("User " + userName + " declined your request :(")
    elif option == 'Q':
        c.send(b"Bye")
        c.close()
        globalListener.close()
        break
