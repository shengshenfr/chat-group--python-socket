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
    
def disconnectionRequest(sequenceNum,sourceID):
    messageType = 10
    R = 0     
    A = 0 
    value = valueControl(messageType,R,sequenceNum,A)
    groupID = 0
    disconnectionRequest = ctypes.create_string_buffer(5)
    struct.pack_into('>BBBH', disconnectionRequest, 0,value,sourceID,groupID,0x0006)  
    
    return disconnectionRequest


def userListRequest(sequenceNum,sourceID):
    messageType = 3
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNum,A)
 
    userListRequest = ctypes.create_string_buffer(5)
    struct.pack_into('bbbH', userListRequest, 0,value,sourceID,0x01,0x0006) 

def sendDataMessage(data,sequenceNum):
    messageType = 5
    R = 0     
    A = 0
    value = valueControl(messageType,R,sq,A)
    sourceID = getClientID(data)
    groupID = getGroupID(data)
    
    print("please input payload")
    
    payload = raw_input()
    print("payload : " + str(payload))
    payloadLength = len(payload)
    print("payloadLength : " + str(payloadLength))
    dataMessage = struct.pack('>BBBHH' + str(len(payload)) + 's', value, sourceID, groupID,0x0008,len(payload),payload)
    print(dataMessage)
    

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
            
            
    elif(messageType == 0x01):
        if(sequenceNumReceived == sequenceNumSend):     
            sequenceNumberSend = (sequenceNumberSend + 1)%2
            
            print("it is connectionReject")
            Error = getError(data)
            if Error == 1:
                print("uername already taken")
            else :
                print("maximum number of users exceeded")
                
    else:            
            
            
            
    
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
        data,addr1 = s.recvfrom(1024)        
        print(data)
        type = getType(data)
        sq =  getSequenceNumber(data)
        ACK = getACK(data)          
        
    
else:
    
    while True:
        print("are you want to connect, please input the type")
        type = input()
        if type == 0:
            
            
        else :     
            
            disconnectionRequest = disconnectionRequest(sequenceNum,data,sourceID,A)
                
            
            
            
            
            
            