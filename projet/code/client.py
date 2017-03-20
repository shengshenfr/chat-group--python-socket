import socket
import sys,os
import select
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


clientID =0
groupID = 0
sourceID = 0
Qmsg = Queue()
ACK = 0
messageType = 0
clientIDList = []
userList = {}
ID_invited_list = []
groupID_private = 0
typeServer = 1

def valueControl(messageType,R,S,ACK):
#    print("R :" + str(R))
#    print("S :" + str(S))
#    print("ACK :" + str(ACK))
    value = messageType<<1    
#    print("value1 :" +str(bin(value)))
    value = value + R <<1
#    print(value)
#    print("value2 :" + str(bin(value)))
    value = value + S <<1 
#    print("value3 :" + str(bin(value)))
    value = value + ACK  
    
    return int(value)  
    


def getError(Reject):
    Error = struct.unpack('>B', Reject,6)
    e = Error>>7
    return e
 
    
def getType(data):       
    premier = struct.unpack('>B', data[0])
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
#    print ("Premier element : " + str(premier[0]))
#    print ("Premier element en binaire : " + str(bin(premier[0])))    
    
    s = str(bin(premier[0]))

    n = len(s)
    print("n:"+str(n))  
    sequenceNum = s[n-2]
    print("senquenceNum:"+sequenceNum)
    
    return int(sequenceNum)
    
def getACK(data):
    premier = struct.unpack('>B', data[0])
#    print ("Premier element : " + str(premier[0]))
#    print ("Premier element en binaire : " + str(bin(premier[0])))    
    S = str(bin(premier[0]))
    print("S:"+S)
    n = len(S)
    print("n:"+str(n)) 
    A = S[n-1]
    print("ACK:"+A)
    
    return int(A)
        
    
def getClientID(Accept):
    clientID = struct.unpack_from('>B', Accept,5)

    print("clientID :" +str(clientID[0])) 

    return clientID[0]
    

def getGroupID(data):    
    groupID = struct.unpack_from('>B', data,2)
    print("groupID : " + str(groupID[0]))
    
    return groupID[0]   

def getGroupID_private(data):
    groupID_private = struct.unpack_from('>B', data,8)
    print("groupID private: " + str(groupID_private[0]))
    
    return groupID_private[0]     

def getSourceID(data):
    sourceID = struct.unpack_from('>B', data,7)
    print("sourceID: " + str(sourceID[0]))
    
    return sourceID[0]     

def getTypeServer(groupCreationRequest):
    typeServer = struct.unpack_from('>B', groupCreationRequest,6)
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
    global userList,clientIDList
    
    userFormat = '>BBBH'+str(len(userListResponse)-5)+'s'
    user = ctypes.create_string_buffer(len(userListResponse))
    user = struct.unpack_from(userFormat, userListResponse,0)
    print("user : "+ str(user[4]))
    userList = eval(user[4])
    
    for key in userList.items():
        clientIDList.append(key[0])
        

    print("userlist transfered from string to dict :" +str(userList))    
    print("clientIDList in getUserList :"+str(clientIDList))
    return userList 
#    clientID = struct.unpack_from('B', userListResponse,5)
#    clientID = clientID[0]    
#    print("clientID in dict : "+ str(clientID)) 
#    
#    groupID = struct.unpack_from('B', userListResponse,6)
#    groupID = groupID[0] 
#    print("groupID in dict : "+ str(groupID))  
#    
#    username = struct.unpack_from('8s', userListResponse,7)
#    username = username[0].decode('UTF-8')
#    print("username in dict : "+ str(username))  
    
#    ipAddress = struct.unpack_from('L', userListResponse,9)
#    ipAddress = ipAddress[0]
#    print("ipAddress in dict : "+ str(ipAddress))
#    
#    port = struct.unpack_from('H', userListResponse,10)
#    port = ipAddress[0]
#    print("port in dict : "+ str(port)) 
    
#    userList = {}.fromkeys([username])
##    userList[username] =  [clientID,groupID,(ipAddress,port)]    
#    userList[username] =  [clientID,groupID]
#    usernameList.append(username)    
#    print("userList : "+ str(userList))  
#    print("usernameList : "+ str(usernameList))
           
    

def acknowledgement():
    global clientID,ACK,sequenceNumReceived
    R = 0     

    value = valueControl(messageType,R,sequenceNumReceived,ACK)

    acknowledgement = ctypes.create_string_buffer(5)
    struct.pack_into('>BBBH', acknowledgement, 0,value,clientID,0x00,0x0005)  
    return acknowledgement

    
def connection(s,addr):
    print("are you want to connect, please input your username")
    username = raw_input()
    print("username :" +str(username))
    if len(username) <=8:
        n = len(username)
        print("n:"+str(n))
        username = username + (8-n)*'0'
        print("username :" +str(username))
        connect = ctypes.create_string_buffer(14)
        #put data into the buffer
        struct.pack_into('>BBBH8s', connect, 0,0x00,0x00,0x00,0x000E,str(username).encode('UTF-8'))
        s.sendto(connect,addr)
    else:
        print("nom is over the length, pls reconnect")

    return  connect
    
def disconnectionRequest():
    global clientID,sequenceNumSend,messageType
    print("disconnect sq: " +str(sequenceNumSend))
    messageType = 0x10
    R = 0     
    A = 0 
    value = valueControl(messageType,R,sequenceNumSend,A)
    print(bin(value))
    groupID = 0
    disconnectionRequest = ctypes.create_string_buffer(6)
    struct.pack_into('>BBBH', disconnectionRequest, 0,value,clientID,groupID,0x0005)  
    
    return disconnectionRequest


def userListRequest():
    global clientID,messageType,sequenceNumSend
    messageType = 3
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNumSend,A)
 
    userListRequest = ctypes.create_string_buffer(6)
    struct.pack_into('>BBBH', userListRequest, 0,value,clientID,0x01,0x0006)
    return userListRequest    
    

def sendDataMessage(payload):
    global messageType,sequenceNumSend,clientID,groupID
    messageType = 5
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNumSend,A)    

#    payloadLength = len(payload)
#    print("payloadLength : " + str(payloadLength))
    dataMessage = struct.pack('>BBBHH' + str(len(payload)) + 's', value, clientID, groupID,0x0008,len(payload),payload)
    print(dataMessage)
    
    return dataMessage
 
 
def groupCreationRequest(ID_invited_list):
    
    global messageType,sequenceNumSend,clientID
    
    messageType  = 6
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNumSend,A)
    print("choose server mode, 1 for centralized, 0 for decentralized")
    T = raw_input()
    T = int(T)    
    if T == 1:
        print("group centralized")
    else :
        print("group decentralized")
        
    T = T <<7
    
    clientInvited = str(ID_invited_list)
    length = len(ID_invited_list) + 6
    
#    groupCreationRequest = ctypes.create_string_buffer(9)
    groupCreationRequest = struct.pack('>BBBHB'+str(len(clientInvited))+'s',value,clientID,0x00,length,T,clientInvited)

    return groupCreationRequest      

def clientGroupInvitationRequest():
    global sequenceNum,clientID,groupID,typeServer
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
    struct.pack_into('>BBBHBB', groupInvitationRequest, 0,value,clientID,0x00,0x0008,typeServer,groupID) 

    
  
def groupInvitationAccept():
    global sequenceNumSend,clientID,groupID_private,typeServer,sourceID
    messageType = 10
    R = 0     
    A = 1
    value = valueControl(messageType,R,sequenceNumSend,A)
    if typeServer == 1:
        print("group centralized")
    else :
        print("group decentralized")
        
    typeServer = typeServer <<7
    print("clientID in group invitation accept : "+str(clientID))    
    print("sourceID in group invitation accept : "+str(sourceID))
    groupInvitationAccept = ctypes.create_string_buffer(9)
    struct.pack_into('>BBBHBBB', groupInvitationAccept, 0,value,sourceID,0x00,0x0008,typeServer,groupID_private,clientID) 
    
    return groupInvitationAccept

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
    global sequenceNumSend,sequenceNumReceived

    global userList,usernameList
    global clientID, groupID, ACK, messageType,typeServer,groupID_private,sourceID
    
    messageType = getType(data)
    print("messageType : "+ str(messageType) )
    sequenceNumReceived =  getSequenceNumber(data)
    print("sequenceNumReceived : "+ str(sequenceNumReceived) )
    print("sequenceNumSend before: " + str(sequenceNumSend))
#    print("groupID : "+ str(groupID)) 
    ACK = getACK(data)    
    print("ACK : "+ str(ACK) ) 
    print("userList in dataReceived : "+ str(userList))
#    groupID_private = getGroupID_private(data)
#    print("groupID_private : " + str(groupID_private))
    
    if (messageType == 0x01):
        if(sequenceNumReceived == sequenceNumSend):
            sequenceNumSend = (sequenceNumSend + 1)%2
            print("sequenceNumSend after : " + str(sequenceNumSend))
            print("it is connectionAccept")

            groupID = getGroupID(data)
            clientID = getClientID(data)  
            print("clientID in 0x01: "+ str(clientID))
#            sourceID = getClientID(data)
            print("groupID in 0x01: "+ str(groupID))
            print("ACK in 0x01 :"  +str(ACK))          
            acknow = acknowledgement()
            s.sendto(acknow,addr)            
            
            
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
            
    elif(messageType == 0x04 and ACK ==1 ):
        if(sequenceNumReceived == sequenceNumSend):

            
            print("it is userList respond")
#            sourceID = getClientID(data)
#            print("clientID : "+ str(clientID))
            userList = getUserList(data)
            
            print("userList in 0x04 : "+ str(userList))            
            
            acknow = acknowledgement()
            s.sendto(acknow,addr) 
            return messageType       

    elif(messageType == 0x05 and ACK ==1):
        if(sequenceNumReceived == sequenceNumSend):

            
            print("ACK of server transfer the message  ")
            print("ACK in 0x0A :"  +str(ACK))          
             
#            clientID = getClientID(data)
#            print("clientID : "+ str(clientID))
            
            
    elif(messageType == 0x07 and ACK ==1 ):
        if(sequenceNumReceived == sequenceNumSend):

            
            print("server creation accepted")
            print("clientID in 0x07 : "+str(clientID))            
            print("groupID_private in 0x07 : "+str(groupID_private))
            print("userList in 0x07 before: "+ str(userList))
#            sourceID = getClientID(data)
#            print("clientID : "+ str(clientID))
            userList[clientID][1] = groupID_private
            groupID = groupID_private          
            print("userList in 0x07 after: "+ str(userList))             
            acknow = acknowledgement()
            s.sendto(acknow,addr)
            print("I have received server creation accepted")            
            
            return messageType    

    elif(messageType == 0x0A and ACK ==1 ):
        if(sequenceNumReceived == sequenceNumSend):

            
            print("server transfered invitation accepted")
            print("clientID in 0x0A : "+str(clientID))
            print("groupID_private in 0x07 : "+str(groupID_private))
            print("userList in 0x0A before: "+ str(userList))
#            sourceID = getClientID(data)
#            print("clientID : "+ str(clientID))
            userList[clientID][1] = groupID_private
            groupID = groupID_private          
            print("userList in 0x0A after: "+ str(userList))
            acknow = acknowledgement()
            s.sendto(acknow,addr)             
            print("join a group success")
  
                
              
    elif(messageType == 0x10 and ACK ==1):
        if(sequenceNumReceived == sequenceNumSend):

            
            print("it is disconnection ACK")
            print("ACK in 0x10 :"  +str(ACK))          
            acknow = acknowledgement()
            s.sendto(acknow,addr)              
#            clientID = getClientID(data)
#            print("clientID : "+ str(clientID))
            
            print("session end")
            s.close()
            sys.exit()   
            
            
    elif(messageType == 0x11):
            
            print(" serverTransferGroupInvitation from client %s" %clientID)
            print("ACK in 0x11 :"  +str(ACK))          
            sourceID = getSourceID(data)
            print("messageType in 0x11 :" + str(messageType))
            print("sourceID in 0x11 :" +str(sourceID))
            groupInvA = groupInvitationAccept()

            s.sendto(groupInvA,addr)              
#            clientID = getClientID(data)
#            print("clientID : "+ str(clientID))
            
      

    else:
        print("wait")
#    elif():
#       
#        
#    elif():    

       
#    else:            
            
            
            
    


print("connection")
connect = connection(s,addr)
inputs = [s, sys.stdin]

while True :
    readable,writable,exceptional = select.select(inputs,[],[], 10)
    for r in readable:
        if s==r:
            
#            global sequenceNumSend,sequenceNumReceived
#        
#            global userList,usernameList
#            global clientID, groupID, ACK, messageType,typeServer,groupID_private,sourceID
            
            data,addr = s.recvfrom(1024)
            print(data)
            messageType = getType(data)
            print("messageType : "+ str(messageType) )
            sequenceNumReceived =  getSequenceNumber(data)
            print("sequenceNumReceived : "+ str(sequenceNumReceived) )
            print("sequenceNumSend before: " + str(sequenceNumSend))
        #    print("groupID : "+ str(groupID)) 
            ACK = getACK(data)    
            print("ACK : "+ str(ACK) ) 
#            print("userList in dataReceived : "+ str(userList))
        #    groupID_private = getGroupID_private(data)
        #    print("groupID_private : " + str(groupID_private))
            
            if (messageType == 0x01):
                if(sequenceNumReceived == sequenceNumSend):
                    sequenceNumSend = (sequenceNumSend + 1)%2
                    print("sequenceNumSend after : " + str(sequenceNumSend))
                    print("it is connectionAccept")
        
                    groupID = getGroupID(data)
                    clientID = getClientID(data)  
                    print("clientID in 0x01: "+ str(clientID))
        #            sourceID = getClientID(data)
                    print("groupID in 0x01: "+ str(groupID))
                    print("ACK in 0x01 :"  +str(ACK))          
                    acknow = acknowledgement()
                    s.sendto(acknow,addr)            
                    
                    
                             
                    
            elif(messageType == 0x02):
                if(sequenceNumReceived == sequenceNumSend):     
                    sequenceNumSend = (sequenceNumSend + 1)%2
                    
                    print("it is connectionReject")
                    Error = getError(data)
                    if Error == 1:
                        print("uername already taken")
                    else :
                        print("maximum number of users exceeded")
                    
                    
            elif(messageType == 0x04 and ACK ==1 ):
                if(sequenceNumReceived == sequenceNumSend):
        
                    
                    print("it is userList respond")
        #            sourceID = getClientID(data)
        #            print("clientID : "+ str(clientID))
                    userList = getUserList(data)
                    
                    print("userList in 0x04 : "+ str(userList))            
                    
                    acknow = acknowledgement()
                    s.sendto(acknow,addr) 
    
        
            elif(messageType == 0x05 and ACK ==1):
                if(sequenceNumReceived == sequenceNumSend):
        
                    
                    print("ACK of server transfer the message  ")
                    print("ACK in 0x0A :"  +str(ACK))          
                     
        #            clientID = getClientID(data)
        #            print("clientID : "+ str(clientID))
                    
                    
            elif(messageType == 0x07 and ACK ==1 ):
                if(sequenceNumReceived == sequenceNumSend):
        
                    
                    print("server creation accepted")
                    print("clientID in 0x07 : "+str(clientID))            
                    print("groupID_private in 0x07 : "+str(groupID_private))
                    print("userList in 0x07 before: "+ str(userList))
        #            sourceID = getClientID(data)
        #            print("clientID : "+ str(clientID))
                    userList[clientID][1] = groupID_private
                    groupID = groupID_private          
                    print("userList in 0x07 after: "+ str(userList))             
                    acknow = acknowledgement()
                    s.sendto(acknow,addr)
                    print("I have received server creation accepted")            
                    
 
        
            elif(messageType == 0x0A and ACK ==1 ):
                if(sequenceNumReceived == sequenceNumSend):
        
                    
                    print("server transfered invitation accepted")
                    print("clientID in 0x0A : "+str(clientID))
                    print("groupID_private in 0x07 : "+str(groupID_private))
                    print("userList in 0x0A before: "+ str(userList))
        #            sourceID = getClientID(data)
        #            print("clientID : "+ str(clientID))
                    userList[clientID][1] = groupID_private
                    groupID = groupID_private          
                    print("userList in 0x0A after: "+ str(userList))
                    acknow = acknowledgement()
                    s.sendto(acknow,addr)             
                    print("join a group success")
          
                        
                      
            elif(messageType == 0x10 and ACK ==1):
                if(sequenceNumReceived == sequenceNumSend):
        
                    
                    print("it is disconnection ACK")
                    print("ACK in 0x10 :"  +str(ACK))          
                    acknow = acknowledgement()
                    s.sendto(acknow,addr)              
        #            clientID = getClientID(data)
        #            print("clientID : "+ str(clientID))
                    
                    print("session end")
                    s.close()
                    sys.exit()   
                    
                    
            elif(messageType == 0x11):
                    
                    print(" serverTransferGroupInvitation from client %s" %clientID)
                    print("ACK in 0x11 :"  +str(ACK))          
                    sourceID = getSourceID(data)
                    print("messageType in 0x11 :" + str(messageType))
                    print("sourceID in 0x11 :" +str(sourceID))
                    groupInvA = groupInvitationAccept()
        
                    s.sendto(groupInvA,addr)              
        #            clientID = getClientID(data)
        #            print("clientID : "+ str(clientID))
                    
              
        
            else:
                print("wait")
#            print("userList"+str(userList)
        else :
            print ("chose type to do")
            mType = sys.stdin.readline().strip()
            if mType:
                if (mType == 'A'):
                    sequenceNumSend = (sequenceNumSend + 1)%2
                    print("sequenceNumSend in main: "+ str(sequenceNumSend))
                    print("userListRequest")
                    userListRequest = userListRequest()
                    s.sendto(userListRequest,addr)
                    
                elif(mType == 'C'):
                    sequenceNumSend = (sequenceNumSend + 1)%2
                    print("group creation request")
        #            print("userList in group Creation Request : "+str(userList))
                    print("who do you want to invite, pls input clientID, and end with 0")
                    ID = raw_input()
                    while ID != '0':    
                        ID_int = int(ID)
                        ID_invited_list.append(ID_int)
                        ID = raw_input()
                        
                    print("ID in group creation request : " + str(ID_invited_list))            
                    
                    
                    groupCreationRequest = groupCreationRequest(ID_invited_list)
                    s.sendto(groupCreationRequest,addr)
            
                    
                elif(mType == 'D'):
                    sequenceNumSend = (sequenceNumSend + 1)%2
                    print("disconnection")
        #                print(sourceID)
                    sequenceNumSend = (sequenceNumSend + 1)%2
                    print("sequenceNumSend in main: "+ str(sequenceNumSend)) 
                    disconnectionRequest = disconnectionRequest()
                    s.sendto(disconnectionRequest,addr)
                    
                    
                elif(mType == 'E'):
                    sequenceNumSend = (sequenceNumSend + 1)%2            
                    print("send a message in public")
                    print("please input payload")
            
                    payload = raw_input()
                    print("payload : " + str(payload))
                    dataMessage = sendDataMessage(payload)
        
                    s.sendto(dataMessage,addr)            
                else:
                    print("what do you want to do")                
            
#childPid = os.fork()
#
#
#if childPid ==0:
#    while True:
#        data,addr = s.recvfrom(1024)
#        print(data)
#        dataReceived(s,data,addr)
#        print("userList"+str(userList))
#        
#        Qmsg.put([clientID, groupID ,sourceID, messageType, sequenceNumSend, ACK, userList, groupID_private]) 
#        print(str(Qmsg.qsize()))
#        print("iiiiiiiiii")
#
#else:
#    while True:
#
#        print("pls input Yes to update")
#        message = raw_input()
#        if message =='Yes': 
#            if not Qmsg.empty():
#                print("azert")
#                synchr = Qmsg.get()
#                clientID = synchr[0] 
#                print("clientID in main : "+ str(clientID))
#                   
#                groupID = synchr[1]
#                print("groupID in main : "+ str(groupID))
#                   
#                sourceID = synchr[2]
#                print("sourceID in main : "+ str(sourceID))
#                   
#                messageType = synchr[3]
#                print("messageType in main : "+ str(messageType))
#             
#                sequenceNumSend = synchr[4]
#                print("sequenceNumSend in main: "+ str(sequenceNumSend))
#              
#                ACK = synchr[5]
#                print("ACK in main: "+ str(ACK))
#            
#                userList = synchr[6]
#                print("userList in main: "+ str(userList))
#                
#                groupID_private = synchr[7]
#                print("groupID_private in main: "+ str(groupID_private))
#            
#                
#            print ("chose type to do")
#            mType = raw_input()
#    
#    
#            if (mType == 'A'):
#                sequenceNumSend = (sequenceNumSend + 1)%2
#                print("sequenceNumSend in main: "+ str(sequenceNumSend))
#                print("userListRequest")
#                userListRequest = userListRequest()
#                s.sendto(userListRequest,addr)
#                
#            elif(mType == 'C'):
#                sequenceNumSend = (sequenceNumSend + 1)%2
#                print("group creation request")
#    #            print("userList in group Creation Request : "+str(userList))
#                print("who do you want to invite, pls input clientID, and end with 0")
#                ID = raw_input()
#                while ID != '0':
#                    ID_int = int(ID)
#                    ID_invited_list.append(ID_int)
#                    ID = raw_input()
#                    
#                print("ID in group creation request : " + str(ID_invited_list))            
#                
#                
#                groupCreationRequest = groupCreationRequest(ID_invited_list)
#                s.sendto(groupCreationRequest,addr)
#        
#                
#            elif(mType == 'D'):
#                sequenceNumSend = (sequenceNumSend + 1)%2
#                print("disconnection")
#    #                print(sourceID)
#                sequenceNumSend = (sequenceNumSend + 1)%2
#                print("sequenceNumSend in main: "+ str(sequenceNumSend)) 
#                disconnectionRequest = disconnectionRequest()
#                s.sendto(disconnectionRequest,addr)
#                
#                
#            elif(mType == 'E'):
#                sequenceNumSend = (sequenceNumSend + 1)%2            
#                print("send a message in public")
#                print("please input payload")
#        
#                payload = raw_input()
#                print("payload : " + str(payload))
#                dataMessage = sendDataMessage(payload)
#    
#                s.sendto(dataMessage,addr)            
#            else:
#                print("what do you want to do")
           
            
            
            
            