import socket
import sys,os
import select

def connectionAccept():
    data,addr = s.recvfrom(1024)
    premier = struct.unpack('>b', data[0])
    print ("Premier element : " + str(premier[0]))
    print ("Premier element en binaire : " + str(bin(premier[0])))
    
    username = struct
    
    print("please distribuer client ID")
    ID = input()
    if len(ID) <= 12:
        n = len(ID)
        ID =  (12-n)*'0'+ ID
        print ("ID"+str(ID))
    Accept = ctypes.create_string_buffer(19)
    struct.pack_into('bbbH12sb', Accept, 0,0b00001000,0x00,0x00,0x0000,str(ID).encode('UTF-8'),0x0)

#    premier=struct.unpack('bbbH12sb', Accept)
#    print ("element : " + str(premier))
#    print( len(Accept))
    s.sendto(Accept,addr)


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
	    #receiver
	    premier = struct.unpack('b', data[0])
	    print ("Premier element : " + str(premier[0]))
	    print ("Premier element en binaire : " + str(bin(premier[0])))

	    chaine = struct.unpack('3s', buf[1:4])
	    print ("Voici la chaine de caracteres : " + chaine[0].decode('UTF-8') 
	    if c = 
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


    