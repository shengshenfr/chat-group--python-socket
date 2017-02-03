import socket
import threading


PORT = 1220
HOST = 'localhost'

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)	
s.bind((HOST,PORT))
s.listen(10)

print ("Serveur : %s:%s" %(HOST,PORT))
print ("wait connexion")


while True:
    connection,addr = s.accept()
    connection2,addr = s.accept()
    connection.send('welcome to server!')
    message = "begin"
    while message != "finish":
        message = connection.recv(1024)
        print(message)
        connection2.send("I received "+message)
        #message = connection.recv(1024)
        
    connection.send('Bye!')    
    connection.close()
    exit()	
        