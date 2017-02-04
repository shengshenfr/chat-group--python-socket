import socket
import threading

PORT = 1251
HOST = 'localhost'

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)	
s.bind((HOST,PORT))
s.listen(10)

print ("Serveur : %s:%s" %(HOST,PORT))
print ("wait connexion")

while True:
    conn,addr = s.accept()
    print 'connected by',addr
    def forum(conn):    
        while True:
            data = conn.recv(1024)
            print '%s says: %s ' %(addr,data)
            reply = raw_input("reply un message:  ")
            conn.send(reply)
    
    
    t = threading.Thread(target = forum, args=[conn])
    t.start()
s.close()