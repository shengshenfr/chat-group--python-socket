import socket
import sys,os
import select
import ctypes
import struct
import argparse

import time
from socerr import socerr 


PORT = 1250
HOST = 'localhost'
addr = (HOST,PORT)
#s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s = socerr(socket.AF_INET, socket.SOCK_DGRAM,0)
s.connect((HOST,PORT))




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
#    print("messageType:"+str(messageType))
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
#    print("n:"+str(n))  
    sequenceNum = s[n-2]
#    print("senquenceNum:"+sequenceNum)
    
    return int(sequenceNum)
    
def getACK(data):
    premier = struct.unpack('>B', data[0])
#    print ("Premier element : " + str(premier[0]))
#    print ("Premier element en binaire : " + str(bin(premier[0])))    
    S = str(bin(premier[0]))
#    print("S:"+S)
    n = len(S)
#    print("n:"+str(n)) 
    A = S[n-1]
#    print("ACK:"+A)
    
    return int(A)
        
    
def getClientID(Accept):
    clientID = struct.unpack_from('>B', Accept,5)

#    print("clientID :" +str(clientID[0])) 

    return clientID[0]
    

def getGroupID(data):    
    groupID = struct.unpack_from('>B', data,2)
    print("groupID : " + str(groupID[0]))
    
    return groupID[0]   

def getGroupID_private(data):
    groupID_private = struct.unpack_from('>B', data,8)
    print("groupID private: " + str(groupID_private[0]))
    
    return groupID_private[0]  
    
def getID_private(data):
    groupID_private = struct.unpack_from('>B', data,6)
    print("groupID private: " + str(groupID_private))
    
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
#    print("clientID before : "+ str(clientID)) 
    payload = getPayload[5]
#    print("payload : " + str(payload) )
    
    return payload

def getUserList(userListResponse):
    global userList,clientIDList
    user_info = []
    length_user = (len(userListResponse)-5)/16
    print(length_user)
    userFormat = '>BBBHBB8sLH'
    user = ctypes.create_string_buffer(len(userListResponse))
    offset = 0
    for offset in length_user : 
        user = struct.unpack_from(userFormat, userListResponse,offset)
        offset += 1
        user_info.append(user)  
    
    userList = eval(user[4])
    
    for key in userList.items():
        clientIDList.append(key[0])
        

#    print("userlist transfered from string to dict :" +str(userList))    
#    print("clientIDList in getUserList :"+str(clientIDList))
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
    
    global sequenceNumReceived,userID
    R = 0     
    A = 1
    value = valueControl(messageType,R,sequenceNumReceived,A)

    acknowledgement = ctypes.create_string_buffer(5)
    struct.pack_into('>BBBH', acknowledgement, 0,value,userID,0x00,0x0005)  
    return acknowledgement

    
def connection(s,addr):
    print("are you want to connect, please input your username")
    username = raw_input()
    print("username :" +str(username))
    
#    connect = ctypes.create_string_buffer(14)
        #put data into the buffer
    connect = struct.pack('>BBBH8s',0x00,0x00,0x00,0x000E,username)
    s.sendto(connect,addr)
#    sendData(connect,addr)

    return  username
    
def disconnectionRequest():
    global userID,sequenceNumSend,messageType
    print("disconnect sq: " +str(sequenceNumSend))
    messageType = 0x10
    R = 0     
    A = 0 
    value = valueControl(messageType,R,sequenceNumSend,A)
#    print(bin(value))
    groupID = 0
    disconnectionRequest = ctypes.create_string_buffer(6)
    struct.pack_into('>BBBH', disconnectionRequest, 0,value,userID,groupID,0x0005)  
    
    return disconnectionRequest


def userListRequest():
    global userID,messageType,sequenceNumSend,addr_sequenceNum_ACK
    messageType = 3
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNumSend,A)

    userListRequest = ctypes.create_string_buffer(6)
    struct.pack_into('>BBBH', userListRequest, 0,value,clientID,0x01,0x0006)
    return userListRequest    
    

def sendDataMessage(payload):
    global messageType,sequenceNumSend,userID,groupID,addr_sequenceNum_ACK
    messageType = 5
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNumSend,A)    

#    payloadLength = len(pay#sequenceNumReceived =  getSequenceNumber(data)load)
#    print("payloadLength : " + str(payloadLength))
    dataMessage = struct.pack('>BBBHH' + str(len(payload)) + 's', value, userID, groupID,0x0008,len(payload),payload)
    print(dataMessage)
    
    return dataMessage
    
    

        
 
def groupCreationRequest(ID_invited_list):
    
    global messageType,sequenceNumSend,userID
    
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
    groupCreationRequest = struct.pack('>BBBHB'+str(len(clientInvited))+'s',value,userID,0x00,length,T,clientInvited)
 
    return groupCreationRequest      

def clientGroupInvitationRequest(ID,group_invited):
    global sequenceNumSend,typeServer,userID
    messageType = 9 
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNumSend,A)
    if typeServer == 1:
        print("group centralized")
    else :
        print("group decentralized")
        
    typeServer = typeServer <<7

    groupInvitationRequest = ctypes.create_string_buffer(9)
    struct.pack_into('>BBBHBBB', groupInvitationRequest, 0,value,userID,0x00,0x0008,typeServer,group_invited,ID) 
    return groupInvitationRequest
    
  
def groupInvitationAccept():
    global sequenceNumSend,userID,groupID_private,typeServer,sourceID
    messageType = 10
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNumSend,A)
    if typeServer == 1:
        print("group centralized")
    else :
        print("group decentralized")
        
    typeServer = typeServer <<7
    print("userID in group invitation accept : "+str(userID))    
    print("sourceID in group invitation accept : "+str(sourceID))
    groupInvitationAccept = ctypes.create_string_buffer(9)
    struct.pack_into('>BBBHBBB', groupInvitationAccept, 0,value,sourceID,0x00,0x0007,typeServer,groupID_private,userID) 
    
    return groupInvitationAccept

def groupInvitationReject():
    global sequenceNumSend,userID,groupID_private,typeServer,sourceID
    messageType = 11
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNumSend,A)
    if typeServer == 1:
        print("group centralized")
    else :
        print("group decentralized")
        
    typeServer = typeServer <<7
    print("userID in group invitation accept : "+str(userID))    
    print("sourceID in group invitation accept : "+str(sourceID))

    groupInvitationReject = ctypes.create_string_buffer(9)
    struct.pack_into('>BBBHBBB', groupInvitationReject, 0,value,sourceID,0x00,0x0007,typeServer,groupID_private,userID)
    return groupInvitationReject

def groupDisjointRequest():
    global messageType, sequenceNumSend,userID
    messageType = 0x0C
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNumSend,A)

    groupDisjointRequest = ctypes.create_string_buffer(6)
    struct.pack_into('BBBH', groupDisjointRequest, 0,value,userID,0x00,0x0005) 
    return groupDisjointRequest

def retransmission(s,addr,buf,messageType_ref,waitTime):
    global messageType, sequenceNumReceived,ACK,resendTimeMax,sequenceNumSend
    resendtime = 1
    temps_break = 1
    time.sleep(2)
    while True:
        resendtime += 1
        readable,writable,exceptional = select.select(inputs,[],[],0.5)       
        for r in readable:
            # open the packet
            data,addr_from = s.recvfrom(1024)
            #print(data)
            messageType = getType(data)
#            print("messageType : "+ str(messageType) ) 
            sequenceNumReceived =  getSequenceNumber(data)
            ACK = getACK(data)
            #jiebao,success,break
            if(messageType == messageType_ref and ACK ==1):
                if(sequenceNumReceived == sequenceNumSend):
                    print("##############################################")
                    print("no need to retransmission")                 
                    temps_break = 4
                    break
        if temps_break >2:
            break
        s.sendto(buf,addr)
        print("this is %s resendtime" %(resendtime-1))
        print("##############################################")
                        
                    ## wait 5s for client to reconnecter
        time.sleep(waitTime)
        if resendtime>resendTimeMax:
            print("the last packet lost")
            return
#def dataReceived(s,data,addr):
#    global sequenceNumSend,sequenceNumReceived
#
#    global userList,usernameList
#    global clientID, groupID, ACK, messageType,typeServer,groupID_private,sourceID
#    
#    messageType = getType(data)



#def retransmission(s,inputs,data,addr):
#global messageType,sequenceNumReceived ,ACK, groupID, userID
#resendTime = 0   
#while True:
#    readable,writable,exceptional = select.select(inputs,[],[],0.5)
#    exit_flag = False
#
#    for r in readable:
#        # open the packet
#        data,addr = s.recvfrom(1024)
#        #print(data)
#        messageType = getType(data)
#        print("messageType : "+ str(messageType) ) 
#        sequenceNumReceived =  getSequenceNumber(data)
#        ACK = getACK(data)
#        #jiebao,success,break
#        if (messageType == 0x04 and ACK == 1):
#            
#            print("it is userList respond")
##            sourceID = getClientID(data,userList)
##            print("clientID : "+ str(clientID))
#            userList = getUserList(data)
#            
#            print("userList in 0x04 : "+ str(userList))                        
#            break
#                        
#    if exit_flag:
#        break
#    while resendtime<2:
#        dataSended(s,addr)
#        
#        print("packet loss, this is  %s  resendtime"%(resendtime+1))
#        resendtime = resendtime +1
#        print("stop operation")         
            
sequenceNumSend = 0
sequenceNumReceived = 0


clientID =0
groupID = 0
sourceID = 0
#Qmsg = Queue()
ACK = 0
messageType = 0
clientIDList = []
userList = {}
ID_invited_list = []
groupID_private = 0
typeServer = 1
userID = 0
timeout = 3
resendTimeMax = 5
resendMessage = {}
addr_type_sequenceNum_ACK = {}
messageTypeList = ['A','B','C','D','E','F','O']
inputs = [s, sys.stdin]
thread_buf = {}

            
while True :          
    print("connection") 
    username = connection(s,addr)
#    print("your username is : " +str(username))

    resendtime = 0
    temps_break = 1
    ## every 6s to reconnection
    time.sleep(5) 
    while True:
        resendtime += 1
        readable,writable,exceptional = select.select(inputs,[],[],0.5)

        for r in readable:
            # open the packet
            data,addr = s.recvfrom(1024)
            #print(data)
            messageType = getType(data)
            print("messageType : "+ str(messageType) ) 
            sequenceNumReceived =  getSequenceNumber(data)
            ACK = getACK(data)
            print("ACK : "+ str(ACK) ) 
            #jiebao,success,break
            if (messageType == 0x01 and ACK == 1):
                
                print("it is connectionAccept")
    
                groupID = getGroupID(data)
                userID = getClientID(data)  
                print("userID in 0x01: "+ str(userID))
                #            sourceID = getClientID(data)
                print("groupID in 0x01: "+ str(groupID))

                print("receive packet connection accept and send ack")
                
                acknow = acknowledgement()
                s.sendto(acknow,addr)                
                
                temps_break = 4
                break
            elif (messageType == 0x02 and ACK == 1):
                temps_break = 3
                print("it is connectionReject")
                acknow = acknowledgement()
                s.sendto(acknow,addr)
                print("receive packet connection reject and send ack")
        if temps_break >2:
            break
        
        
        username = connection(s,addr)
        print("this is %s resendtime" %resendtime)
 
        if resendtime>resendTimeMax:
            print("the last packet lost")        
            s.close()    
            exit() 
    if temps_break >3:

        break 
        
    else :
        #################### if client does not receive the packet , it need to wait 2s to resend
        time.sleep(1)
        

#            print("packet loss, this is  %s  resendtime"%(resendtime+1))
#            resendtime = resendtime +1
#            print("stop connection")
#            exit()

    

    #print("sequenceNumReceived : "+ str(sequenceNumReceived) )
    #print("sequenceNumSend before: " + str(sequenceNumSend))
    



while True :

    readable,writable,exceptional = select.select(inputs,[],[])
    for r in readable:
        # ######################receive
        if s==r:
            
#            global sequenceNumSend,sequenceNumReceived
#        
#            global userList,usernameList
#            global clientID, groupID, ACK, messageType,typeServer,groupID_private,sourceID
            
            data,addr_from = s.recvfrom(1024)
            print(data)
            messageType = getType(data)
            print("messageType : "+ str(messageType) )
            sequenceNumReceived =  getSequenceNumber(data)
            print("sequenceNumReceived : "+ str(sequenceNumReceived) )

            print("sequenceNumSend : " + str(sequenceNumSend))
        #    print("groupID : "+ str(groupID)) 
            ACK = getACK(data)    
            print("ACK : "+ str(ACK) ) 
#            print("userList in dataReceived : "+ str(userList))
        #    groupID_private = getGroupID_private(data)
        #    print("groupID_private : " + str(groupID_private))
            

            # determiner if i have received a new or old packet
            
            flag = False
            if addr_from not in addr_type_sequenceNum_ACK:
                print ("stock this packet")
                addr_type_sequenceNum_ACK [addr_from] = [messageType,sequenceNumReceived,ACK]
            else :
                if (addr_type_sequenceNum_ACK [addr_from][0] == messageType) and (addr_type_sequenceNum_ACK [addr_from][1] == sequenceNumReceived):
                    print("i have received this packet")
                    flag = True
    
                else :
                    print ("i have never received this packet")
                    addr_type_sequenceNum_ACK [addr_from] = [messageType,sequenceNumReceived,ACK]
                           
            print("111111")
            if flag == False:  
                print("222222")
                if(messageType == 0x04 and ACK ==1):
                    if(sequenceNumReceived == sequenceNumSend):
                        print("##############################################")
                        print("it is userList respond")
            #            sourceID = getClientID(data,userList)
            #            print("clientID : "+ str(clientID))
                        userList = getUserList(data)
                        
                        print("userList in 0x04 : "+ str(userList))            
                        
                        acknow = acknowledgement()
                        s.sendto(acknow,addr)
                       
                        
    
                if(messageType == 0x05 and ACK == 0 ):
                    if(sequenceNumReceived == sequenceNumSend):
                        print("##############################################")
                        print("i have received the message that server transfers  ")
                        print("ACK in 0x05 :"  +str(ACK))
                        payload = getPayload(data)
                        print("payload in 0x05 :"+str(payload))
                        acknow = acknowledgement()
                        s.sendto(acknow,addr)
            #            clientID = getClientID(data)
            #            print("clientID : "+ str(clientID))
                        
                        
    
    #    clientID = struct.unpack_from('B', Accept,5)%s
#######################################"  group creation success
                elif(messageType == 0x07 ):
                    
            
                    print("##############################################")
                     
                    print("server creation accepted")
                    
                    print("userID in 0x07 : "+str(userID))
#                        print("sourceID in 0x07 : "+str(sourceID))
                    groupID_private = getID_private(data)
                    print("groupID_private in 0x07 : "+str(groupID_private))
                    print("userList in 0x07 before: "+ str(userList))
        #            sourceID = getClientID(data)
        #            print("clientID : "+ str(clientID))
                                            
                    
                    userList[userID][1] = groupID_private
#                    userList[sourceID][1] = groupID_private
#                        userList[sourceID][1] = groupID_private
                    groupID = groupID_private 
                    print("userList in 0x07 after: "+ str(userList))             
                    acknow = acknowledgement()
                    s.sendto(acknow,addr)
                    print("ACK in 0x07 : "+str(ACK)) 
                    print("I have received server creation accepted")        
                    print("##############################################")
                        
                        
 #######################################  group creation failed                       
                elif(messageType == 0x08 and ACK==0):
#                    if(sequenceNumReceived == sequenceNumSend):
                    print("##############################################")
                     
                    print("server creation refused")
                    print("ID_invited_list : "+ str(ID_invited_list))
                    ID_invited_list = []
                    print("after delete the client, ID_invited_list : "+ str(ID_invited_list))  
                    acknow = acknowledgement()
                    s.sendto(acknow,addr)
                    print("##############################################")
                        



#######################################  client join a group success 
                elif(messageType == 0x0A and ACK ==1 ):
                    if(sequenceNumReceived == sequenceNumSend):
            
                        print("##############################################")
                        print("join a group success")
#                        print("userID in 0x0A : "+str(userID))         
#                        print("groupID_private in 0x07 : "+str(groupID_private))
#                        print("userList in 0x0A before: "+ str(userList))
#            #            sourceID = getClientID(data)
#            #            print("clientID : "+ str(clientID))
#                        userList[userID][1] = groupID_private
#                        groupID = groupID_private          
#                        print("userList in 0x0A after: "+ str(userList))
                        
                        acknow = acknowledgement()
                        s.sendto(acknow,addr)
                        print("ACK in 0x0A : "+str(ACK)) 
                        print("##############################################")
                        
                        
 #######################################"  client refuse invitation sucess         
                elif(messageType == 0x0B and ACK ==1 ):
                    if(sequenceNumReceived == sequenceNumSend):
            
                        print("##############################################")
                        print("refuse invitation sucess")
                        print("##############################################")
                        
                        
                elif(messageType == 0x0E and ACK == 0):
                    
                    print("##############################################")
                    print("update userList broadcast from client")
        #            sourceID = getClientID(data,userList)
        #            print("clientID : "+ str(clientID))
                    userList = getUserList(data)
                    
                    print("userList in 0x0E : "+ str(userList))            
                    
                    acknow = acknowledgement()
                    s.sendto(acknow,addr)
                    print("##############################################")
                
                elif(messageType == 0x0F and ACK == 0):
                    if(sequenceNumReceived == sequenceNumSend):
                        print("##############################################")
                        print("update disconnection broadcast from client")
            #            sourceID = getClientID(data,userList)
            #            print("clientID : "+ str(clientID))
                        
                        
                        print("old userList in 0x0E : "+ str(userList))            
                        clientID_quit = getClientID(data)
                        print("clientID_quit : "+str(clientID_quit))
                        del userList[clientID_quit]
                        print("new userList : " +str(userList))                          
                        acknow = acknowledgement()
                        s.sendto(acknow,addr)
                        print("##############################################")             
                        
####################################### disconnection                          
                elif(messageType == 0x10 and ACK ==1):
                    if(sequenceNumReceived == sequenceNumSend):
            
                        print("##############################################")
                        print("it is disconnection ACK")
    
    #    clientID = struct.unpack_from('B', Accept,5)
                        print("ACK in 0x10 :"  +str(ACK))         
                        acknow = acknowledgement()
                        s.sendto(acknow,addr)              
            #            clientID = getClientID(data)
            #            print("clientID : "+ str(clientID))
                        
                        print("session end")
                        s.close()    
                        exit()   
                        
                        
                elif(messageType == 0x11):
                        print("##############################################")
                        sourceID = getSourceID(data)
                        print("sourceID in 0x11 :" +str(sourceID))
                        print(" serverTransferGroupInvitation from client %s" %sourceID)
                        print("ACK in 0x11 :"  +str(ACK))          
                        
    
    #    clientID = struct.unpack_from('B', Accept,5)
                        print("messageType in 0x11 :" + str(messageType))
                        
                        print("ACK in 0x11 :"  +str(ACK))          
                        sourceID = getSourceID(data)
                        
                        
#                        acknow = acknowledgement()
#                        s.sendto(acknow,addr)
#                        time.sleep(0.2)
                        
                        print("choose if you acepet an invitation, Y or N")
                        mes = raw_input()
                        if mes =='Y':
                            print("agree to join a group private")
                            groupInvA = groupInvitationAccept()
                            s.sendto(groupInvA,addr)
                        else : 
                            print("refuse invitation")
                            groupInvR = groupInvitationReject()
                            s.sendto(groupInvR,addr)
            #            clientID = getClientID(data)%s
            #            print("clientID : "+ str(clientID))
                        
        #            print("userList"+str(userList)
                        
                        
   ###################################################################################sender                     
        else :
            print("##############################################")
            print ("chose type to do")
            mType = sys.stdin.readline().strip()


            if (mType == 'A'):
                sequenceNumSend = (sequenceNumSend + 1)%2   
                print("sequenceNumSend in main: "+ str(sequenceNumSend))
                print("userListRequest")
                userListRequest = userListRequest()
                s.sendto(userListRequest,addr)
                messageType_ref = 0x04
                waitTime = 3 
                retransmission(s,addr,userListRequest,messageType_ref, waitTime)
#                stopFlag = Event()
#                thread = MyThread(stopFlag,s,addr,buf,sequenceNumSend)
#                thread.start()
##                message = raw_input("Please enter your message: ")
#                thread_buf[userID] = thread

                # retransmission                
#                retransmission(s,addr,userListRequest)
                
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

                print("sequenceNumSend in main: "+ str(sequenceNumSend)) 
                disconnectionRequest = disconnectionRequest()
                s.sendto(disconnectionRequest,addr)
                messageType_ref = 0x10
                
                resendtime = 0
                temps_break = 1
                time.sleep(2)
                while True:
                    resendtime += 1
                    readable,writable,exceptional = select.select(inputs,[],[],0.5)         
                    for r in readable:
                        # open the packet
                        data,addr = s.recvfrom(1024)
                        #print(data)
                        messageType = getType(data)
            #            print("messageType : "+ str(messageType) ) 
                        sequenceNumReceived =  getSequenceNumber(data)
                        ACK = getACK(data)
                        #jiebao,success,break
                        if(messageType == 0x10 and ACK ==1):
                            if(sequenceNumReceived == sequenceNumSend):
            
                                print("##############################################")
                                print("it is disconnection ACK")
                                temps_break = 4
                                break
                        if temps_break >2:
                            break
                        s.sendto(disconnectionRequest,addr)
                        print("this is %s resendtime" %resendtime)
                        if resendtime>resendTimeMax:
                            print("the last packet lost")
                if temps_break >3:
                    break 
                
            elif(mType == 'E'):
                sequenceNumSend = (sequenceNumSend + 1)%2  
                print("send a message in public")
                print("please input payload")
 
                payload = raw_input()
                print("payload : " + str(payload))
                dataMessage = sendDataMessage(payload)
    
                s.sendto(dataMessage,addr)
                resendtime = 0
                temps_break = 1
                time.sleep(10)
                while True:
                    resendtime += 1
                    readable,writable,exceptional = select.select(inputs,[],[],0.5)         
                    for r in readable:
                        # open the packet
                        data,addr = s.recvfrom(1024)
                        #print(data)
                        messageType = getType(data)
            #            print("messageType : "+ str(messageType) ) 
                        sequenceNumReceived =  getSequenceNumber(data)
                        ACK = getACK(data)
                        #jiebao,success,break
                        if(messageType == 0x05 and ACK ==1):
                            if(sequenceNumReceived == sequenceNumSend):
                                print("##############################################")
                                print("ACK of server transfer the message success ")
#                                print("ACK in 0x0A :"  +str(ACK))                                             
#                                acknow = acknowledgement()
#                                s.sendto(acknow,addr)
                                temps_break = 4
                                break
                    if temps_break >2:
                        break
                    s.sendto(dataMessage,addr)
                    print("this is %s resendtime" %resendtime)
                    if resendtime>resendTimeMax:
                        print("the last packet lost")
                if temps_break >3:
                    break                           
                                
            elif(mType == 'disjoint'):
                sequenceNumSend = (sequenceNumSend + 1)%2  
                print("i want to leave the private group")

                groupDR = groupDisjointRequest()
    
                s.sendto(groupDR,addr)
                
            elif(mType == 'invite'):
                sequenceNumSend = (sequenceNumSend + 1)%2  
                print("i want to invite another client")
                print("userList in main : "+str(userList))
                print("my userID in main : "+str(userID))
                print("pls input client you want to invite")
                ID = raw_input()
                ID = int(ID)
                ################# get group private
                group_invited = userList[userID][1]
                groupInvitationRequest =  clientGroupInvitationRequest(ID,group_invited)
                s.sendto(groupInvitationRequest,addr)
    
                
                
                
            else:
                print("wait")       
                

            
#childPid = os.fork()
#
#
#if childPid ==0:            data,addr = s.recvfrom(1024)
#            print(data)
#            messageType = getType(data)
#            print("messageType : "+ str(messageType) )
#            sequenceNumReceived =  getSequenceNumber(data)
#            print("sequenceNumReceived : "+ str(sequenceNumReceived) )
#            print("sequenceNumSend before: " + str(sequenceNumSend))
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
#                sequenceNumSend = (sequenceNumSend + 1)u%2
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
#                from socerr import socerr 
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
           
            
            
            
            