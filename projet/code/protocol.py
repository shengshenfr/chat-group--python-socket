import ctypes
import struct
import argparse







//youwenti
def userListResponse(sourceID,ipAddress,port):
    type = 4
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 0
    value = valueControl(type,R,sq,A)
    headerLength
    userListResponse = ctypes.create_string_buffer(5)
    struct.pack_into('bbbH', userListResponse, 0,value,sourceID,0x01,headerLength) 

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



def getPayload(dataMessage):    
    bufFormat= '>BBBHH' + str(len(dataMessage) - 7) + 's'
    getPayload = ctypes.create_string_buffer(len(dataMessage))
    getPayload = struct.unpack_from(bufFormat, dataMessage, 0)

    payload = getPayload[5]
    print("payload : " + str(payload) )
    
    return payload

//youwenti
def groupCreationRequest(sequenceNum,sourceID,T,clientID):
    messageType  = 6
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 0
    value = valueControl(messageType,R,sq,A)
    T = T <<7
    userListRequest = ctypes.create_string_buffer(7)
    struct.pack_into('bbbHbb', userListRequest, 0,value,sourceID,0x00,0x0008,T,clientID)     
     
     
def groupCreationAccept(sequenceNum,sourceID,T,groupID):
    messageType  = 7
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 0
    value = valueControl(messageType,R,sq,A)
    T = T <<7
    userListRequest = ctypes.create_string_buffer(7)
    struct.pack_into('bbbHbb', userListRequest, 0,value,sourceID,0x00,0x0008,T,groupID) 
    

def groupCreationReject(sequenceNum,sourceID):
    messageType  = 8
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 0
    value = valueControl(messageType,R,sq,A)

    userListRequest = ctypes.create_string_buffer(5)
    struct.pack_into('bbbH', userListRequest, 0,value,sourceID,0x00,0x0006) 
    

def groupInvitationRequest(sequenceNum,sourceID,T,groupID):
    messageType = 9
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 0
    value = valueControl(messageType,R,sq,A)
    T = T <<7
    userListRequest = ctypes.create_string_buffer(7)
    struct.pack_into('bbbHbb', userListRequest, 0,value,sourceID,0x00,0x0008,T,groupID) 
        
    
def groupInvitationAccept(sequenceNum,sourceID,T,groupID):
    messageType = 10
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 0
    value = valueControl(messageType,R,sq,A)
    T = T <<7
    userListRequest = ctypes.create_string_buffer(7)
    struct.pack_into('bbbHbb', userListRequest, 0,value,sourceID,0x00,0x0008,T,groupID) 

def groupInvitationReject():
    messageType = 11
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 0
    value = valueControl(messageType,R,sq,A)
    T = T <<7
    userListRequest = ctypes.create_string_buffer(7)
    struct.pack_into('bbbHbb', userListRequest, 0,value,sourceID,0x00,0x0008,T,groupID)     
    

def groupDisjointRequest():
    messageType = 12
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 0
    value = valueControl(messageType,R,sq,A)

    userListRequest = ctypes.create_string_buffer(5)
    struct.pack_into('bbbH', userListRequest, 0,value,sourceID,0x00,0x0006) 

def groupDissolution(sequenceNum,groupID):
    messageType = 13
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 0
    value = valueControl(messageType,R,sq,A)
    acknowledgement = ctypes.create_string_buffer(5)
    struct.pack_into('>BBBH', acknowledgement, 0,value,0x00,groupID,0x0006)  



def updateList():



def updateDisconnection(sequenceNum,clienID):
    messageType = 15
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 0
    value = valueControl(messageType,R,sq,A)
    acknowledgement = ctypes.create_string_buffer(6)
    struct.pack_into('>BBBHB', acknowledgement, 0,value,0x00,0xFF,0x0008,clientID)  
    
    

def acknowledgement(messageType,sequenceNumReceived,sourceID):
    R = 0     
    A = 1
    value = valueControl(messageType,R,sequenceNumReceived,A)
    groupID = 0x00
    acknowledgement = ctypes.create_string_buffer(5)
    struct.pack_into('>BBBH', acknowledgement, 0,value,sourceID,groupID,0x0006)  















