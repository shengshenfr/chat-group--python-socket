import socket
import sys,os
import select
import ctypes
import struct
import argparse

PORT = 1250
HOST = 'localhost'

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)	
s.bind((HOST,PORT))

inputs = [s]
address = []
usernameList = []
userList = {}
clientID = 0
groupID =0x01
sequenceNumReceived = 0
groupPrivateList = []

def valueControl(messageType,R,S,ACK):
    value = messageType<<1    
#    print(bin(value))
    value = value + R <<1
#    print(value)
    value = value + S <<1 
    value = value + ACK 
    print("value : "+ str(value))
    return int(value)  
    


def getError(Reject):
    Error = struct.unpack('>b', Reject,6)
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
    if premier[0]==0:
        sequenceNum =0
    else:
        s = str(bin(premier[0]>>1))
        print(s)
        n = len(s)
        print("n:"+str(n))  
        sequenceNum = s[n-1]
        
    print("senquenceNum:"+str(sequenceNum))
    
    return int(sequenceNum)

    
def getACK(data):
    premier = struct.unpack('>b', data[0])
#    print ("Premier element : " + str(premier[0]))
#    print ("Premier element en binaire : " + str(bin(premier[0])))    
    S = str(bin(premier[0]))
    print("S:"+str(S))
    n = len(S)
    print("n:"+str(n)) 
    A = S[n-1]
    print("ACK:"+A)
    
    return int(A)
        
    
def getClientID(Accept):
    ID = struct.unpack_from('b', Accept,5)
    clientID = ID[0]
    print(clientID) 

    return clientID
    

def getGroupID(data):    
    groupID = struct.unpack_from('b', data,3)
    print(groupID)
    
    return groupID   


def getTypeServer(groupCreationRequest):
    typeServer = struct.unpack_from('b', groupCreationRequest,6)
    print(typeServer)
    typeServer = typeServer >>7
    print(typeServer)
    return int(typeServer) 

def getSourceID(Accept):
    sourceID = struct.unpack_from('b', Accept,3)
    sourceID = sourceID[0]
    print(sourceID) 

    return sourceID
    
    
def getPayload(dataMessage):    
    bufFormat= '>BBBHH' + str(len(dataMessage) - 7) + 's'
    getPayload = ctypes.create_string_buffer(len(dataMessage))
    getPayload = struct.unpack_from(bufFormat, dataMessage, 0)

    payload = getPayload[5]
    print("payload : " + str(payload) )
    
    return payload    
    
    
def acknowledgement():
    global messageType, A,sequenceNumReceived
    R = 0     
    A = 1
    value = valueControl(messageType,R,sequenceNumReceived,A)

    acknowledgement = ctypes.create_string_buffer(5)
    struct.pack_into('>BBBH', acknowledgement, 0,value,clientID,0x00,0x0005) 
    return acknowledgement

def connectionAccept(data):
    global clientID,groupID,messageType,sequenceNumReceived
    global userList,usernameList
    # response
    messageType = 1
    R = 0 
    A = 1
    
    value = valueControl(messageType ,R,sequenceNumReceived,A)
    print("please distribuer client ID")
    print("clientID before : "+ str(clientID))   
    clientID = clientID + 1   
    print("clientID after: "+ str(clientID))  
    username = getUsername(data)
    print("username : "+ str(username))
    usernameList.append(username)
    print("usernameList : "+ str(usernameList))
#    userList = {}.fromkeys([clientID])
    
#        print("userList1 : "+ str(userList)) 

     
    print("groupID : "+ str(groupID))
     
    userList[clientID] =  [username,groupID,addr]
    print("userList : "+ str(userList)) 



#    print ("groupID : "+str(groupID))
#    print ("clientID : "+str(clientID))

    Accept = ctypes.create_string_buffer(6)
    struct.pack_into('>BBBHB', Accept, 0,value,0x00,groupID,0x0000,clientID)
    print(Accept)

#    clientID = struct.unpack_from('B', Accept,5)
#
#    print("fuck :" +str(clientID))
    
    
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
    struct.pack_into('>BBBHB', Reject, 0,value,0x00,0x00,0x0007,Error) 
    
    return Reject


def sendUserListResponse():
    global usernameList,userList
    type = 4
    R = 0     
    A = 1
    value = valueControl(type,R,sequenceNumReceived,A)
    length = len(userList) + 5
    print("usernameList : "+str(usernameList))    
    print("userList : "+str(userList))
    userListString = str(userList)
    print("userListString : "+str(userListString))
#    for iUser in usernameList:
#        print("iUser:"+str(iUser))
#        username = str(iUser)
#        clientID = int(userList[iUser][0])
#        print("clientID in dict : "+ str(clientID)) 
#        groupID  = int(userList[iUser][1])
#        print("groupID in dict : "+ str(groupID))        
#        ipAddress = userList[iUser][2][0]
#        port = int(userList[iUser][2][1])       
#    userListResponse = ctypes.create_string_buffer(21)
    userListResponse = struct.pack('>BBBH'+str(len(userListString))+'s', value,clientID,0x01,length,userListString)
        
    return userListResponse

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
        struct.pack_into('>BBBHBB8s', updateList, 0,value,sourceID,0xFF,length,clientID,groupID,username) 
   
def groupCreationAccept(groupCreationRequest):
    global sequenceNum,groupPrivateList,groupID 
    messageType  = 7
    R = 0     
    A = 1
    value = valueControl(messageType,R,sequenceNum,A)
    
    typeServer = getTypeServer(groupCreationRequest)
    
    if typeServer == 1:
        print("group centralized")
    else :
        print("group decentralized")
        
    typeServer = typeServer <<7
    
    print("distribuer group ID")

    groupID = groupID + 1
    groupPrivateList.append(groupID)
    
    groupCreationAccept = ctypes.create_string_buffer(7)
    
    struct.pack_into('>BBBHBB', groupCreationAccept, 0,value,clientID,0x00,0x0007,typeServer,groupID) 
    

def groupCreationReject():
    global sequenceNum,clientID
    messageType  = 8
    R = 0     
    A = 1
    value = valueControl(messageType,R,sequenceNum,A)

    groupCreationReject = ctypes.create_string_buffer(5)
    struct.pack_into('>BBBH', groupCreationReject, 0,value,clientID,0x00,0x0005) 


def serverTransferGroupInvitation():
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
    struct.pack_into('bbbHbb', groupInvitationRequest, 0,value,clientID,0x00,0x0008,typeServer,groupID)     


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
    value = valueControl(messageType,R,sequenceNum,A)
    userList.remove(clientID)

    updateDisconnection = ctypes.create_string_buffer(6)
    struct.pack_into('>BBBHB', updateDisconnection, 0,value,0x00,0xFF,0x0008,clientID)  


def dataReceived(s,data,addr):
    global clientID,groupID,messageType
    global sequenceNumReceived
    global userList,usernameList    


    messageType = getType(data)
    print("messageType : "+ str(messageType))
    sequenceNumReceived =  getSequenceNumber(data)
    print("sequenceNumReceived : "+ str(sequenceNumReceived) )
    ACK = getACK(data)    
    print("ACK : "+ str(ACK)) 
#    groupID = getGroupID(data)    
#    print("groupID : "+ str(groupID))     
#    
    if (messageType == 0x00):
        
        print("it is connection from client")
 
        Accept = connectionAccept(data)
        s.sendto(Accept,addr)
        
        return messageType  

    elif(messageType == 0x01 and ACK==1):
        print("ACK in 0x01 :"  +str(ACK))
        print("it is connection ACK from client")
#        sourceID = getSourceID(data)
#        print("sourceID : "+ str(sourceID))

        
    elif(messageType == 0x0A):
        if ACK == 0:
            print("it is disconnection request")
#        sourceID = getSourceID(data)
#        print("sourceID : "+ str(sourceID))

            respond = acknowledgement()
            s.sendto(respond,addr)
        else :
            print("disconnection ACK from client")
        
      
     
    elif (messageType == 0x03):
        
        print("userList Request")

        print("clientID : "+ str(clientID))
        print("userlist sended : " + str(userList))
        userListResponse = sendUserListResponse()
        s.sendto(userListResponse,addr)
        
        
    elif(messageType == 0x04 and ACK==1):
        print("ACK in 0x04 :"  +str(ACK))
        print("client %s has received userList respond" %clientID)        
        
#    elif (messageType == 0x05):
#        
#        print("transfer a message from client")
#
#        print("clientID : "+ str(clientID))
#        print("userlist sended : " + str(userList))
#        userListResponse = sendUserListResponse()
#        s.sendto(userListResponse,addr)    

    else:
        
        print("ACK from client")
#        print("clientID : "+ str(clientID))
#        print("groupID : "+ str(groupID)) 



    


#userList[username] = [ip, port, clientID,groupID] 


readable,writable,exceptional = select.select(inputs,[],[], 10)    

#print(str(readable) + '\n')

#print(str(inputs) + '\n')

while True : 
    for r in readable:	
        if s==r:
            data,addr = s.recvfrom(1024)

#            print (data)

            #print(str(data) + '\n')
            address.append(addr)
            if data !="end":
                print ('connected by',addr)
                messageType = getType(data)
                if (messageType == 0x05):
                    print("transfer a message from client")
                    respond = acknowledgement()
                    s.sendto(respond,addr)
                    for i in address:
                        if i is not addr:

                            s.sendto(data,i)
                            
                            
                if (messageType == 0x06): 
                    print("transfer an invitation to another client")
                    
                                             
                else : 
                    dataReceived(s,data,addr)

                #print(str(inputs) + '\n')


            else:
                address.remove(addr)
                if len(address)==0:
                    s.close()
                    sys.exit()