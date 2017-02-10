import socket
import sys,os


PORT = 1239
HOST = 'localhost'

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)	
s.bind((HOST,PORT))
s.listen(10)

print ("Serveur : %s:%s" %(HOST,PORT))
print ("wait connexion")



connection1,addr = s.accept()
connection2,addr = s.accept()
connection1.send('welcome to server!')
connection2.send('welcome to server!')
print("ok")
childPid = os.fork()

if childPid ==0:
    while True:
        message1 = connection1.recv(1024)
        if message1:
            connection2.send(message1)
else:
    while True:
        message2 = connection2.recv(1024)
        if message2:
            connection1.send(message2)
    