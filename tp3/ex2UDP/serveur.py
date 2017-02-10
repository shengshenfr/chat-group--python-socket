import socket
import sys,os
import select

PORT = 1248
HOST = 'localhost'

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)	
s.bind((HOST,PORT))

inputs = [s]
address = []
#while True:
    
  
readable,writable,exceptional = select.select(inputs,[],[], 10)

#print(str(readable) + '\n')

#print(str(inputs) + '\n')

while True : 
    for r in readable:	
	if s==r:
	    
	    data,addr = s.recvfrom(1024)
	    print data
	    
	    #print(str(addr) + '\n')
	    #print(str(data) + '\n')
	    address.append(addr)
	    if data =="end":
	    #print(str(inputs) + '\n')
		address.remove(addr)
		if len(address)==0:
		    s.close()
		    sys.exit()
	    else:
		for i in address:
		    if i is not addr:
		        s.sendto(data,i)


    