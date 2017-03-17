import socket
import sys,os
import select
import ctypes
import struct
import argparse
from protocol import *




def connectionAccept(sequenceNum,clientID,groupID):

    # response
    messageType = 1
    R = 0 
    A = 1
    
    value = valueControl(messageType ,R,sequenceNum,A)

    print("please distribuer client ID")

    print ("clientID : "+str(clientID))

    Accept = ctypes.create_string_buffer(7)
    struct.pack_into('bbbHb', Accept, 0,0b00001000,0x00,groupID,0x0000,clientID)
    print(Accept)

#    ID = struct.unpack_from('b', Accept,6)
#    clientID = ID[0]
#    print(clientID)
    
    
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


def sendUserListResponse(sequenceNum,sourceID,userList):
    type = 4
    R = 0     
    A = 1
    value = valueControl(type,R,sequenceNum,A)
    
    numberUsers = len(userList)
    length = 5 + numberUsers
    for iUser in numberUsers:
        clientID = userList[iUser].clentID
        groupID = userList[iUser].groupID
        username = userList[iUser].username
        userListResponse = ctypes.create_string_buffer(length)
        struct.pack_into('bbbHbb8s', userListResponse, 0,value,sourceID,0x01,length,clientID,groupID,username) 

def updateList(sequenceNum,userList):
    type = 14
    R = 0     
    A = 0
    value = valueControl(type,R,sequenceNum,A)
    sourceID = 0x00
    
    numberUsers = len(userList)
    length = 5 + numberUsers
    for iUser in numberUsers:
        clientID = userList[iUser].clentID
        groupID = userList[iUser].groupID
        username = userList[iUser].username
        updateList = ctypes.create_string_buffer(length)
        struct.pack_into('bbbHbb8s', updateList, 0,value,sourceID,0xFF,length,clientID,groupID,username) 
   
def groupCreationAccept(sequenceNum,groupCreationRequest,sourceID):
    messageType  = 7
    R = 0     
    A = 1
    value = valueControl(messageType,R,sq,A)
    
    typeServer = getTypeServer(groupCreationRequest)
    if typeServer == 1:
        print("group centralized")
    else :
        print("group decentralized")
        
    typeServer = typeServer <<7
    print("please distribuer group ID")
    groupID = raw_input()
    groupID = int(groupID)
    
    groupCreationAccept = ctypes.create_string_buffer(7)
    struct.pack_into('bbbHbb', groupCreationAccept, 0,value,sourceID,0x00,0x0008,typeServer,groupID) 
    

def groupCreationReject(sequenceNum,sourceID):
    messageType  = 8
    R = 0     
    A = 1
    value = valueControl(messageType,R,sequenceNum,A)

    groupCreationReject = ctypes.create_string_buffer(5)
    struct.pack_into('bbbH', groupCreationReject, 0,value,sourceID,0x00,0x0006) 


def groupInvitationRequest(sequenceNum,sourceID,typeServer,groupID):
    messageType = 9
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNum,A)
    if typeServer == 1:
        print("group centralized")
    else :
        print("group decentralized")
        
    typeServer = typeServer <<7

    groupInvitationRequest = ctypes.create_string_buffer(7)
    struct.pack_into('bbbHbb', groupInvitationRequest, 0,value,sourceID,0x00,0x0008,typeServer,groupID)     


def groupDissolution(sequenceNum,groupID):
    messageType = 13
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNum,A)
    groupDissolution = ctypes.create_string_buffer(5)
    struct.pack_into('>BBBH', groupDissolution, 0,value,0x00,groupID,0x0006)  


def updateDisconnection(sequenceNum,clientID,userList):
    messageType = 15
    R = 0     
    A = 0
    value = valueControl(messageType,R,sq,A)
    userList.remove(clientID)

    updateDisconnection = ctypes.create_string_buffer(6)
    struct.pack_into('>BBBHB', updateDisconnection, 0,value,0x00,0xFF,0x0008,clientID)  


def dataReceived(data,addr,clientID):
    messageType = getType(data)
    sequenceNumReceived =  getSequenceNumber(data)
    ACK = getACK(data)    
    
    print("it is connection")
    clientID += 1
    print("clientID : "+ str(clientID))
    groupID = 0x01
    connectionAccept(sequenceNumReceived,clientID,groupID)






    

PORT = 1248
HOST = 'localhost'

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)	
s.bind((HOST,PORT))

inputs = [s]
address = []

userList = {}
clientID = 0

#userList[username] = [ip, port, clientID,groupID] 


readable,writable,exceptional = select.select(inputs,[],[], 10)    

#print(str(readable) + '\n')

#print(str(inputs) + '\n')

while True : 
    for r in readable:	
	if s==r:
	    
	    data,addr = s.recvfrom(1024)
	    print data
            dataReceived(data,addr,clientID)
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
    