import socket
import threading

PORT = 1220
HOST = 'localhost'


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))

while True:
    #message = "hello"
    #s.send(message)
    #while message != "finish":
        #print("you want to send what?")
        #message = raw_input()
        #s.send(message)
    #message = "client_em"
    #s.send(message)
    mes = s.recv(1024)
    print(mes)
    #s.send("finish")
s.close()