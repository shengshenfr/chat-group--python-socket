import socket
import sys,os
import ctypes
import struct
import argparse
from protocol import *



    
def connection():
    print("are you want to connect, please input your username")
    username = input()
    if len(username) <=8:
        n = len(username)
        username = username + (8-n)*'0'
        connect = ctypes.create_string_buffer(14)
        #put data into the buffer
        struct.pack_into('BBBH8s', connect, 0,0x00,0x00,0x00,0x000E,str(username).encode('UTF-8'))
    else:
        print("nom is over the length")

    return  connect
    
def disconnectionRequest(sequenceNumSend,sourceID):
    messageType = 10
    R = 0     
    A = 0 
    value = valueControl(messageType,R,sequenceNumSend,A)
    groupID = 0
    disconnectionRequest = ctypes.create_string_buffer(5)
    struct.pack_into('>BBBH', disconnectionRequest, 0,value,sourceID,groupID,0x0006)  
    
    return disconnectionRequest


def userListRequest(sequenceNumSend,sourceID):
    messageType = 3
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNumSend,A)
 
    userListRequest = ctypes.create_string_buffer(5)
    struct.pack_into('bbbH', userListRequest, 0,value,sourceID,0x01,0x0006) 

def sendDataMessage(sequenceNumSend,sourceID,groupID):
    messageType = 5
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNumSend,A)    
    print("please input payload")
    
    payload = raw_input()
    print("payload : " + str(payload))
    payloadLength = len(payload)
    print("payloadLength : " + str(payloadLength))
    dataMessage = struct.pack('>BBBHH' + str(len(payload)) + 's', value, sourceID, groupID,0x0008,len(payload),payload)
    print(dataMessage)
 
 
def groupCreationRequest(sequenceNumSend,sourceID,T,clientID):
    messageType  = 6
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNumSend,A)
    
    if T == 1:
        print("group centralized")
    else :
        print("group decentralized")
        
    T = T <<7
    groupCreationRequest = ctypes.create_string_buffer(7)
    struct.pack_into('bbbHbb', groupCreationRequest, 0,value,sourceID,0x00,0x0008,T,clientID)      
    
  
def groupInvitationAccept(sequenceNum,sourceID,typeServer,groupID):
    messageType = 10
    R = 0     

    A = 1
    value = valueControl(messageType,R,sequenceNum,A)
    typeServer = typeServer <<7
    groupInvitationAccept = ctypes.create_string_buffer(7)
    struct.pack_into('bbbHbb', groupInvitationAccept, 0,value,sourceID,0x00,0x0008,typeServer,groupID) 


def groupInvitationReject(sequenceNum,sourceID):
    messageType = 11
    R = 0     
    A = 1
    value = valueControl(messageType,R,sq,A)

    groupInvitationReject = ctypes.create_string_buffer(7)
    struct.pack_into('bbbHbb', groupInvitationReject, 0,value,sourceID,0x00,0x0008)


def groupDisjointRequest(sequenceNum,sourceID):
    messageType = 12
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNum,A)

    groupDisjointRequest = ctypes.create_string_buffer(5)
    struct.pack_into('bbbH', groupDisjointRequest, 0,value,sourceID,0x00,0x0006) 


def dataReceived(data,addr,sequenceNumSend):

    messageType = getType(data)
    sequenceNumReceived =  getSequenceNumber(data)
    ACK = getACK(data)

    if (messageType == 0x01):
        if(sequenceNumReceived == sequenceNumSend):
            sequenceNumberSend = (sequenceNumberSend + 1)%2
            
            print("it is connectionAccept")
            sourceID = getClientID(data)
            print("clientID : "+ str(sourceID))
            acknowledgement(type,sequenceNumReceived,sourceID)
            groupID = 0x01
            userListRequest(sequenceNumberSend,sourceID)
            
            
    elif(messageType == 0x02):
        if(sequenceNumReceived == sequenceNumSend):     
            sequenceNumberSend = (sequenceNumberSend + 1)%2
            
            print("it is connectionReject")
            Error = getError(data)
            if Error == 1:
                print("uername already taken")
            else :
                print("maximum number of users exceeded")
                
    else:
        if(sequenceNumReceived == sequenceNumSend):
            sequenceNumberSend = (sequenceNumberSend + 1)%2
            
            print("it is userList respond")
            sourceID = getClientID(data)
            print("clientID : "+ str(sourceID))
            acknowledgement(type,sequenceNumReceived,sourceID)
            groupID = 0x01
            userListRequest(sequenceNumberSend,sourceID)
            
#    elif():
#       
#        
#    elif():    

       
#    else:            
            
            
            
    
PORT = 1248
HOST = 'localhost'
addr = (HOST,PORT)
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect((HOST,PORT))


sequenceNumSend = 0
sequenceNumReceived = 0


childPid = os.fork()


if childPid ==0:
    while True:
        data,addr = s.recvfrom(1024)
        print(data)
        dataReceived(data,addr,sequenceNumSend)
        
    
else:
    while True:
        print("you want to send what?")
        message = raw_input()
        if message != "end":
            connect = connection()
            s.sendto(connect,addr)

        else:
            disconnect = disconnectionRequest(sequenceNumSend,sourceID)
            s.sendto(disconnect,addr)
            print("session end")
            s.close()
            sys.exit()                
            
            
            
            
            
            