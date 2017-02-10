import socket
import threading
import sys,os


PORT = 1254
HOST = 'localhost'

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))

childPid = os.fork()


if childPid ==0:
    while True:
        mes = s.recv(1024)

        print(mes)
    
else:
    while True:
        
        print("you want to send what?")
        message = raw_input()
        if message =="end":
            s.send(message)
            print("session end")
            s.close()
            sys.exit()
        else:
            s.send(message)

