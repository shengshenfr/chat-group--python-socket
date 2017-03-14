import socket
import sys,os
import select
import ctypes
import struct
import argparse
from protocol import *







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


    