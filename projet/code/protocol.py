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


def connectionAccept(sequenceNum,ACK):
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
    if len(ID) <= 8:
        n = len(ID)
        ID =  (8-n)*'0'+ ID
        print ("ID"+str(ID))
    
    Accept = ctypes.create_string_buffer(14)
    struct.pack_into('bbbH8s', Accept, 0,value,0x00,0x00,0x0008,str(ID).encode('UTF-8'))
#    premier=struct.unpack('bbbH12sb', Accept)
#    print ("element : " + str(premier))
#    print( len(Accept))


def connectionReject(sequenceNum,ACK,Error):
    # response
    type = 2
    R = 0 
    if (sequenceNum  == 1):
        sq = 0
    else: 
        sq = 1
        
    A = 0
    value = valueControl(type,R,sq,A)
    e = str(Error)
    e = e + 7*'0'
    Reject = ctypes.create_string_buffer(14)
    struct.pack_into('bbbH8s', Reject, 0,value,0x00,0x00,0x0007,e) 
    

def userListRequest():
    

def userListResponse():


def dataMessage():


def groupCreationRequest():


def groupCreationAccept():

def groupCreationReject():

def groupInvitationRequest():

def groupInvitationAccept():


def groupInvitationReject():

def groupDisjointRequest():


def groupDissolution():


def updateList():



def updateDisconnection():

    
    
def disconnectionRequest():



def acknowledgement():
















