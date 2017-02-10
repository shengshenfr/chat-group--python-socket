import socket
import sys,os
import select

PORT = 1254
HOST = 'localhost'

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)	
s.bind((HOST,PORT))
s.listen(10)

print ("Serveur : %s:%s" %(HOST,PORT))
print ("wait connexion")



input = [s]

while True:
    readable,writable,exceptional = select.select(input,[],[])
    for r in readable:	
	if s==r:
	    print ("accept")
	    connexion,addr = r.accept()
            input.append(connexion)

    for r in readable:    
	if r != s:
	    message = r.recv(1024)
	 
	    if message =="end":
		input.remove(r)
		if(len(input))==0:
		    s.close()
		    sys.exit()
	    else:	
		for i in input:
		    if i is not r and i is not s:
		        i.send(message)
	
	
