import socket
import sys,os
import select
import ctypes
import struct
import argparse
from protocol import *



    


def connectionAccept(sequenceNum,A):
    # response
    messageType = 1
    R = 0 
    
    if (A  == 1):
        A = 0
    else: 
        A = 1
    
    value = valueControl(messageType ,R,sequenceNum,A)

    print("please distribuer client ID")
    ID = raw_input()
    ID = int(ID)
    print ("ID : "+str(hex(ID)))

    Accept = ctypes.create_string_buffer(7)
    struct.pack_into('bbbHb', Accept, 0,0b00001000,0x00,0x00,0x0000,ID)
    print(Accept)

    ID = struct.unpack_from('b', Accept,6)
    clientID = ID[0]
    print(clientID)
    
    
    return Accept
#    premier=struct.unpack('bbbH12sb', Accept)
#    print ("element : " + str(premier))
#    print( len(Accept))


def connectionReject(sequenceNum,Error,A):
    # response
    messageType = 2
    R = 0 
    if (A  == 1):
        A = 0
    else: 
        A = 1
        
    value = valueControl(messageType,R,sequenceNum,A)
    if Error == 1:
        print("uername already taken")
    else :
        print("maximum number of users exceeded")
        
    Error = Error<<7
    Reject = ctypes.create_string_buffer(6)
    struct.pack_into('bbbHb', Reject, 0,value,0x00,0x00,0x0007,Error) 
    
    return Reject
    

PORT = 1248
HOST = 'localhost'

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)	
s.bind((HOST,PORT))

inputs = [s]
address = []
#while True:
    

#print(str(readable) + '\n')

#print(str(inputs) + '\n')

while True : 
    data,addr = s.recvfrom(1024)
    print (data)
	    
    #print(str(addr) + '\n')
    #print(str(data) + '\n')
    address.append(addr)        
    type = getType(data)
    sq =  getSequenceNumber(data)
    ACK = getACK(data)
    
    if type == 0:
    #print(str(inputs) + '\n')        
        Accept = connectionAccept
        s.sendto(Accept,addr)

    else:
        
        Reject = connectionReject
        s.sendto(Reject,addr)
    