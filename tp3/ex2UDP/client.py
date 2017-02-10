import socket
import sys,os


PORT = 1248
HOST = 'localhost'
addr = (HOST,PORT)
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect((HOST,PORT))

childPid = os.fork()


if childPid ==0:
    while True:
        mes,addr1 = s.recvfrom(1024)
        print(mes)
    
else:
    while True:
        print("you want to send what?")
        message = raw_input()
        if message == "end":
            s.sendto(message,addr)
            print("session end")
            s.close()
            sys.exit()
        else:
            s.sendto(message,addr)