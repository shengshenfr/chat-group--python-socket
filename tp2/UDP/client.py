import socket


PORT = 1212
HOST = 'localhost'


s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect((HOST,PORT))

while True:
    message = raw_input("input un message:  ")
    s.send(message)
    data = s.recv(1024)
    
    print data