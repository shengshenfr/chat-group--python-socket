import socket
import threading

PORT = 1251
HOST = 'localhost'

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))


while True:
    message = raw_input("input un message:  ")
    s.send(message)
    
    
    data = s.recv(1024)
    print '%s says : %s ' %(HOST,data)
s.close()