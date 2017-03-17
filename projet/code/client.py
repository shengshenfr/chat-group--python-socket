import socket
import sys,os
import ctypes
import struct
import argparse
from multiprocessing import Queue, Process
import time



PORT = 1250
HOST = 'localhost'
addr = (HOST,PORT)
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect((HOST,PORT))


sequenceNumSend = 0
sequenceNumReceived = 0
sourceID = 0
groupID = 0
clientID =0
Qmsg = Queue()




def valueControl(messageType,R,S,ACK):
    value = messageType    
#    print(bin(value))
    value = value + R <<1
#    print(value)
    value = value + S <<1 
    value = value + ACK <<1 
    
    return int(value)  
    


def getError(Reject):
    Error = struct.unpack('>b', Reject,6)
    e = Error>>7
    return e
 
    
def getType(data):       
    premier = struct.unpack('>b', data[0])
#    print ("Premier element : " + str(premier[0]))
#    print ("Premier element en binaire : " + str(bin(premier[0])))
    messageType = premier[0]>>3
    print("messageType:"+str(messageType))
    return messageType


def getUsername(data):
    username = struct.unpack_from('8s', data,6)
    print ("Voici username : " + username[0].decode('UTF-8'))
    username = username[0].decode('UTF-8')        
#    print(username)    
    return username
    
    
def getSequenceNumber(data):
    premier = struct.unpack('>B', data[0])
    print ("Premier element : " + str(premier[0]))
    print ("Premier element en binaire : " + str(bin(premier[0])))    
    
    s = str(bin(premier[0]))

    n = len(s)
    print("n:"+str(n))  
    sequenceNum = s[n-2]
    print("senquenceNum:"+sequenceNum)
    
    return int(sequenceNum)
    
#def getACK(data):
#    premier = struct.unpack('>b', data[0])
#    print ("Premier element : " + str(premier[0]))
#    print ("Premier element en binaire : " + str(bin(premier[0])))    
#    S = str(bin(premier[0]))
#    print("S:"+S)
#    n = len(S)
#    print("n:"+str(n)) 
#    A = S[n-1]
#    print("ACK:"+A)
#    
#    return A
        
    
def getClientID(Accept):
    clientID = struct.unpack_from('>B', Accept,5)

    print("clientID :" +str(clientID[0])) 

    return clientID[0]
    

def getGroupID(data):    
    groupID = struct.unpack_from('>B', data,2)
    print("groupID : " + str(groupID[0]))
    
    return groupID[0]   


def getTypeServer(groupCreationRequest):
    typeServer = struct.unpack_from('b', groupCreationRequest,6)
    print(typeServer)
    typeServer = typeServer >>7
    print(typeServer)
    return typeServer 

def getPayload(dataMessage):    
    bufFormat= '>BBBHH' + str(len(dataMessage) - 7) + 's'
    getPayload = ctypes.create_string_buffer(len(dataMessage))
    getPayload = struct.unpack_from(bufFormat, dataMessage, 0)

    payload = getPayload[5]
    print("payload : " + str(payload) )
    
    return payload

def getUserList(userListResponse):
    userList = struct.unpack_from('16s', userListResponse,5)
    print(userList)
    
    return userList        
    

def acknowledgement(sequenceNumReceived):
    global sourceID
    messageType = 0x11
    R = 0     
    A = 1
    value = valueControl(messageType,R,sequenceNumReceived,A)
    groupID = 0x00
    acknowledgement = ctypes.create_string_buffer(5)
    struct.pack_into('>BBBH', acknowledgement, 0,value,sourceID,groupID,0x0006)  
    return acknowledgement

    
def connection(s,addr):
    print("are you want to connect, please input your username")
    username = raw_input()
    print("username :" +str(username))
    if len(username) <=8:
        n = len(username)
        username = username + (8-n)*'0'
        connect = ctypes.create_string_buffer(14)
        #put data into the buffer
        struct.pack_into('BBBH8s', connect, 0,0x00,0x00,0x00,0x000E,str(username).encode('UTF-8'))
        s.sendto(connect,addr)
    else:
        print("nom is over the length, pls reconnect")

    return  connect
    
def disconnectionRequest():
    global sourceID,sequenceNumSend
    messageType = 10
    R = 0     
    A = 0 
    value = valueControl(messageType,R,sequenceNumSend,A)
    groupID = 0
    disconnectionRequest = ctypes.create_string_buffer(5)
    struct.pack_into('>BBBH', disconnectionRequest, 0,value,sourceID,groupID,0x0005)  
    
    return disconnectionRequest


def userListRequest(sequenceNumSend):
    global sourceID
    messageType = 3
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNumSend,A)
 
    userListRequest = ctypes.create_string_buffer(6)
    struct.pack_into('bbbH', userListRequest, 0,value,sourceID,0x01,0x0006)
    return userListRequest    
    

def sendDataMessage(sequenceNumSend,sourceID,groupID):
    messageType = 5
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNumSend,A)    
    print("please input payload")
    
    payload = input()
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
    value = valueControl(messageType,R,sequenceNum,A)

    groupInvitationReject = ctypes.create_string_buffer(7)
    struct.pack_into('bbbHbb', groupInvitationReject, 0,value,sourceID,0x00,0x0008)


def groupDisjointRequest(sequenceNum,sourceID):
    messageType = 12
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNum,A)

    groupDisjointRequest = ctypes.create_string_buffer(5)
    struct.pack_into('bbbH', groupDisjointRequest, 0,value,sourceID,0x00,0x0006) 


def dataReceived(s,data,addr):
    global sequenceNumSend
    global sourceID
    global clientID
    global groupID
    messageType = getType(data)
    print("messageType : "+ str(messageType) )
    sequenceNumReceived =  getSequenceNumber(data)
    print("sequenceNumReceived : "+ str(sequenceNumReceived) )
    groupID = getGroupID(data)    
    print("groupID : "+ str(groupID)) 
#    ACK = getACK(data)    
#    print("ACK : "+ str(ACK) ) 
 
    
    if (messageType == 0x01):
        if(sequenceNumReceived == sequenceNumSend):
            sequenceNumSend = (sequenceNumSend + 1)%2
            print("sequenceNumSend : " + str(sequenceNumSend))
            print("it is connectionAccept")

            sourceID = getClientID(data)
            print("clientID : "+ str(sourceID))
            ACK = acknowledgement(sequenceNumReceived)
            s.sendto(ACK,addr)
            sourceID = getClientID(data)
            print("clientID : "+ str(sourceID))
            return messageType          
            
    elif(messageType == 0x02):
        if(sequenceNumReceived == sequenceNumSend):     
            sequenceNumSend = (sequenceNumSend + 1)%2
            
            print("it is connectionReject")
            Error = getError(data)
            if Error == 1:
                print("uername already taken")
            else :
                print("maximum number of users exceeded")
            return messageType

                
    elif(messageType == 0x04):
        if(sequenceNumReceived == sequenceNumSend):
            sequenceNumSend = (sequenceNumSend + 1)%2
            
            print("it is userList respond")
            sourceID = getClientID(data)
            print("clientID : "+ str(sourceID))
            
            acknowledgement(type,sequenceNumReceived,sourceID)
            return messageType
            
    else :
        if(sequenceNumReceived == sequenceNumSend):
            sequenceNumSend = (sequenceNumSend + 1)%2
            
            print("it is disconnection ACK")
            sourceID = getClientID(data)
            print("clientID : "+ str(sourceID))
            
            print("session end")
            s.close()
            sys.exit()            
            return messageType
            
#    elif():
#       
#        
#    elif():    

       
#    else:            
            
            
            
    


print("connection")
connect = connection(s,addr)

childPid = os.fork()


if childPid ==0:
    while True:
        data,addr = s.recvfrom(1024)
        print(data)
        messageType = dataReceived(s,data,addr)
        Qmsg.put(sourceID) 
        Qmsg.put(groupID) 
            
else:
    while True:

        
        if not Qmsg.empty():  
            sourceID = Qmsg.get() 
            print("clientID : "+ str(sourceID)) 
            groupID = Qmsg.get()
            print("groupID : "+ str(groupID)) 
            
        print ("chose type to do")
        mType = raw_input()

        if (mType == '3'):
            print("userListRequest")
            userListRequest = userListRequest(sequenceNumSend)        
        else:
            print("disconnection")
#                print(sourceID)
            disconnectionRequest = disconnectionRequest()

            
            
            
            
            
            