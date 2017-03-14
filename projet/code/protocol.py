import ctypes
import struct
import argparse



def connection():
    print("are you want to connect, please input your name")
    username = input()
    if len(username) <=8:
        n = len(username)
        username = username + (8-n)*'0'
        connect = ctypes.create_string_buffer(14)
        #put data into the buffer
        struct.pack_into('BBBH8s', connect, 0,0x00,0x00,0x00,0x000E,str(username).encode('UTF-8'))
            
    else:
        print("nom is over the length")

def disconnectionRequest(sequenceNum,data,sourceID):
    type = 10
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 0
    value = valueControl(type,R,sq,A)
    groupID = 0
    disconnectionRequest = ctypes.create_string_buffer(5)
    struct.pack_into('>BBBH', disconnectionRequest, 0,value,sourceID,groupID,0x0006)  

    


def connectionAccept(sequenceNum):
    # response
    type = 1
    R = 0 
    
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
        
    A = 0
    value = valueControl(type,R,sq,A)

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
#    premier=struct.unpack('bbbH12sb', Accept)
#    print ("element : " + str(premier))
#    print( len(Accept))


def userListRequest(sequenceNum,sourceID):
    type = 3
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 0
    value = valueControl(type,R,sq,A)
 
    userListRequest = ctypes.create_string_buffer(5)
    struct.pack_into('bbbH', userListRequest, 0,value,sourceID,0x01,0x0006) 



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



 
def getType(data):       
    premier = struct.unpack('>b', data[0])
    print ("Premier element : " + str(premier[0]))
    print ("Premier element en binaire : " + str(bin(premier[0])))
    type0 = bin(premier[0]>>3)
    print("type1:"+str(type0))
    return type0

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
    
def valueControl(type,R,S,ACK):
    value = type    
#    print(bin(value))
    value = value + R <<1
#    print(value)
    value = value + S <<1 
    value = value + ACK <<1 
    
    return hex(value)

def connectionReject(sequenceNum,Error):
    # response
    type = 2
    R = 0 
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
        
    A = 0
    value = valueControl(type,R,sq,A)
    if Error == 1:
        print("uername already taken")
    else :
        print("maximum number of users exceeded")
    Reject = ctypes.create_string_buffer(6)
    struct.pack_into('bbbHb', Reject, 0,value,0x00,0x00,0x0007,Error) 
    
    
def getClientID(Accept):
    ID = struct.unpack_from('b', Accept,6)
    clientID = ID[0]
    print(clientID) 

    return clientID
    
         
    
def getGroupID(data):    
    groupID = struct.unpack_from('b', data,4)
    print(groupID)
    
    return groupID   


def dataMessage(data,sequenceNum):
    type = 5
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 0
    value = valueControl(type,R,sq,A)
    sourceID = getClientID(data)
    groupID = getGroupID(data)
    
    print("please input payload")
    
    payload = raw_input()
    print("payload : " + str(payload))
    payloadLength = len(payload)
    print("payloadLength : " + str(payloadLength))
    dataMessage = struct.pack('>BBBHH' + str(len(payload)) + 's', value, sourceID, groupID,0x0008,len(payload),payload)
    print(dataMessage)
    
def getPayload(dataMessage):    
    bufFormat= '>BBBHH' + str(len(dataMessage) - 7) + 's'
    getPayload = ctypes.create_string_buffer(len(dataMessage))
    getPayload = struct.unpack_from(bufFormat, dataMessage, 0)

    payload = getPayload[5]
    print("payload : " + str(payload) )
    
    return payload

//youwenti
def groupCreationRequest(sequenceNum,sourceID,T,clientID):
    type = 6
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 0
    value = valueControl(type,R,sq,A)
    T = T <<7
    userListRequest = ctypes.create_string_buffer(7)
    struct.pack_into('bbbHbb', userListRequest, 0,value,sourceID,0x00,0x0008,T,clientID)     
     
     
def groupCreationAccept(sequenceNum,sourceID,T,groupID):
    type = 7
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 0
    value = valueControl(type,R,sq,A)
    T = T <<7
    userListRequest = ctypes.create_string_buffer(7)
    struct.pack_into('bbbHbb', userListRequest, 0,value,sourceID,0x00,0x0008,T,groupID) 
    

def groupCreationReject(sequenceNum,sourceID):
    type = 8
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 0
    value = valueControl(type,R,sq,A)

    userListRequest = ctypes.create_string_buffer(5)
    struct.pack_into('bbbH', userListRequest, 0,value,sourceID,0x00,0x0006) 
    

def groupInvitationRequest(sequenceNum,sourceID,T,groupID):
    type = 9
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 0
    value = valueControl(type,R,sq,A)
    T = T <<7
    userListRequest = ctypes.create_string_buffer(7)
    struct.pack_into('bbbHbb', userListRequest, 0,value,sourceID,0x00,0x0008,T,groupID) 
        
    
def groupInvitationAccept(sequenceNum,sourceID,T,groupID):
    type = 10
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 0
    value = valueControl(type,R,sq,A)
    T = T <<7
    userListRequest = ctypes.create_string_buffer(7)
    struct.pack_into('bbbHbb', userListRequest, 0,value,sourceID,0x00,0x0008,T,groupID) 

def groupInvitationReject():
    type = 11
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 0
    value = valueControl(type,R,sq,A)
    T = T <<7
    userListRequest = ctypes.create_string_buffer(7)
    struct.pack_into('bbbHbb', userListRequest, 0,value,sourceID,0x00,0x0008,T,groupID)     
    

def groupDisjointRequest():
    type = 12
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 0
    value = valueControl(type,R,sq,A)

    userListRequest = ctypes.create_string_buffer(5)
    struct.pack_into('bbbH', userListRequest, 0,value,sourceID,0x00,0x0006) 

def groupDissolution(sequenceNum,groupID):
    type = 13
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 0
    value = valueControl(type,R,sq,A)
    acknowledgement = ctypes.create_string_buffer(5)
    struct.pack_into('>BBBH', acknowledgement, 0,value,0x00,groupID,0x0006)  



def updateList():



def updateDisconnection(sequenceNum,clienID):
    type = 15
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 0
    value = valueControl(type,R,sq,A)
    acknowledgement = ctypes.create_string_buffer(6)
    struct.pack_into('>BBBHB', acknowledgement, 0,value,0x00,0xFF,0x0008,clientID)  
    
    

def acknowledgement(data,sequenceNum,sourceID):
    type = getType(data)
    R = 0     
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
    A = 1
    value = valueControl(type,R,sq,A)
    groupID = 0
    acknowledgement = ctypes.create_string_buffer(5)
    struct.pack_into('>BBBH', acknowledgement, 0,value,sourceID,groupID,0x0006)  















