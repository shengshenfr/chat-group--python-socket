import socket


PORT = 1212
HOST = 'localhost'

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)	
s.bind((HOST,PORT))
s.listen(10)

print ("Serveur : %s:%s" %(HOST,PORT))
print ("wait connexion")

while True:
    conn,addr = s.accept()
    print 'connected by',addr
    
    while True:
        data = conn.recv(1024)
        print data
        message = raw_input("input un message:  ")
        conn.send(message)