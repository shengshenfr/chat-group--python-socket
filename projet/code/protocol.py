import ctypes
import struct
import argparse



def valueControl(messageType,R,S,ACK):
    value = messageType    
#    print(bin(value))
    value = value + R <<1
#    print(value)
    value = value + S <<1 
    value = value + ACK <<1 
    
    return hex(value)  
    


def getError(Reject):
    Error = struct.unpack('>b', Reject,6)
    e = Error>>7
    return e
 
    
def getType(data):       
    premier = struct.unpack('>b', data[0])
    print ("Premier element : " + str(premier[0]))
    print ("Premier element en binaire : " + str(bin(premier[0])))
    messageType = bin(premier[0]>>3)
    print("messageType:"+str(messageType))
    return messageType


def getUsername(data):
    username = struct.unpack('8s', data[1:9])
    print ("Voici username : " + username[0].decode('UTF-8'))
    username = username[0].decode('UTF-8')        
#    print(username)    
    return username
    
    
def getSequenceNumber(data):
    premier = struct.unpack('>b', data[0])
    print ("Premier element : " + str(premier[0]))
    print ("Premier element en binaire : " + str(bin(premier[0])))    
    S = str(bin(premier[0]))
    print("S:"+S)
    n = len(S)
    print("n:"+str(n))  
    sequenceNum = S[n-2]
    print("senquenceNum:"+sequenceNum)
    
    return sequenceNum

    
def getACK(data):
    premier = struct.unpack('>b', data[0])
    print ("Premier element : " + str(premier[0]))
    print ("Premier element en binaire : " + str(bin(premier[0])))    
    S = str(bin(premier[0]))
    print("S:"+S)
    n = len(S)
    print("n:"+str(n)) 
    A = S[n-1]
    print("ACK:"+A)
    
    return A
        
    
def getClientID(Accept):
    ID = struct.unpack_from('b', Accept,6)
    clientID = ID[0]
    print(clientID) 

    return clientID
    

def getGroupID(data):    
    groupID = struct.unpack_from('b', data,4)
    print(groupID)
    
    return groupID   


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
    userList = []
    userInfomation = ()
    
    offset = 5
    dataLength = struct.unpack_from('H', userListResponse, offset)[0]
    offset = 6
    length = 0
    
    while(length<dataLength):
        clientID = struct.unpack_from('b', userListResponse, offset)[0]
        offset += 1
        groupID = struct.unpack_from('b', userListResponse, offset)[0] 
        offset += 1
        username = struct.unpack_from('8s', userListResponse, offset)[0]
        
        userInfomation = clientID,groupID,username
        userList.append(userInfomation)
    return userList        
    

def acknowledgement(messageType,sequenceNumReceived,sourceID):
    R = 0     
    A = 1
    value = valueControl(messageType,R,sequenceNumReceived,A)
    groupID = 0x00
    acknowledgement = ctypes.create_string_buffer(5)
    struct.pack_into('>BBBH', acknowledgement, 0,value,sourceID,groupID,0x0006)  















