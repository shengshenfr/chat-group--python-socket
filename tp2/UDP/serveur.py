import socket


PORT = 1212
HOST = 'localhost'

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)	
s.bind((HOST,PORT))


print ("Serveur : %s:%s" %(HOST,PORT))
print ("wait connexion")

while True:
    data,addr = s.recvfrom(1024)
    print ('receve from %s%s:' %addr)
    message = raw_input("input un message:  ")
    s.sendto(message,addr)