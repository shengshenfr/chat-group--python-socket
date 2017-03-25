import socket
import sys,os
import select
import ctypes
import struct
import argparse
from socerr import socerr
import time
 
PORT = 1250
HOST = 'localhost'
s = socerr(socket.AF_INET, socket.SOCK_DGRAM, 0)
#s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)	
s.bind((HOST,PORT))


address = []
usernameList = []
userList = {}
clientID = 0
groupID =0x01
sequenceNumSend = 0
sequenceNumReceived = 0
groupPrivateList =  {}
publicList = []
groupID_private = 1
typeServer = 1
sourceID = 0
userID = 0
resendTimeMax = 5

def valueControl(messageType,R,S,ACK):
    value = messageType<<1    
#    print(bin(value))
    value = value + R <<1
#    print(value)
    value = value + S <<1 
    value = value + ACK 
#    print("value : "+ str(value))
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
#    print("messageType:"+str(messageType))
    return messageType


def getUsername(data):
    bufFormat= '>BBBH' + str(len(data) - 5) + 's'
    getUsername = ctypes.create_string_buffer(len(data))
    getUsername = struct.unpack_from(bufFormat, data, 0)
    username = getUsername[4]
#    print ("Voici username : " + username)
         
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
#        print(s)
        n = len(s)
#        print("n:"+str(n))  
        sequenceNum = s[n-1]
        
#    print("senquenceNum:"+str(sequenceNum))
    
    return int(sequenceNum)

    
def getACK(data):
    premier = struct.unpack('>b', data[0])
#    print ("Premier element : " + str(premier[0]))
#    print ("Premier element en binaire : " + str(bin(premier[0])))    
    S = str(bin(premier[0]))
#    print("S:"+str(S))
    n = len(S)
#    print("n:"+str(n)) 
    A = S[n-1]
#    print("ACK:"+A)
    
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

def getSourceID(data):
    sourceID = struct.unpack_from('>B', data,1)
#    print("sourceID: " + str(sourceID))
    
    return sourceID[0]  
    
def getUserID(data):
    userID = struct.unpack_from('>B', data,7)
    print("userID: " + str(userID))
    
    return userID[0]      

def getTypeServer(groupCreationRequest):
    typeServer = struct.unpack_from('B', groupCreationRequest,5)
#    print(typeServer)
    typeServer = typeServer[0] >>7
#    print(typeServer)
    return int(typeServer) 

#def getSourceID(Accept):
#    sourceID = struct.unpack_from('b', Accept,3)
#    sourceID = sourceID[0]
#    print(sourceID) 
#
#    return sourceID
    
    
def getPayload(dataMessage):    
    bufFormat= '>BBBHH' + str(len(dataMessage) - 7) + 's'
    getPayload = ctypes.create_string_buffer(len(dataMessage))
    getPayload = struct.unpack_from(bufFormat, dataMessage, 0)

    payload = getPayload[5]
    print("payload : " + str(payload) )
    
    return payload    
    
def getClientInvited(data):
    bufFormat= '>BBBHB' + str(len(data) - 6) + 's'
    getClientInvited = ctypes.create_string_buffer(len(data))
    getClientInvited = struct.unpack_from(bufFormat, data, 0)
    print(len(getClientInvited))
    print(len(getClientInvited[5]))
    n =  len(getClientInvited[5])    
    clientInvited = list(getClientInvited[5][1:n-1])
    
#    print("getClientInvited : " + str(getClientInvited))
    print("clientInvited : " + str(clientInvited))
    return clientInvited       
    
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
    global userList,usernameList,publicList
    # response
    messageType = 1
    R = 0 
    A = 1
    
    value = valueControl(messageType ,R,sequenceNumReceived,A)
    print("please distribuer client ID")
#    print("clientID before : "+ str(clientID))   
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


def connectionReject(data,Error):
    global messageType,sequenceReceived
    # response
    messageType = 2
    R = 0 
    A = 1
    
    value = valueControl(messageType,R,sequenceNumReceived,A)

    Error = Error<<7
    Reject = ctypes.create_string_buffer(6)
    struct.pack_into('>BBBHB', Reject, 0,value,0x00,0x00,0x0007,Error) 
    
    return Reject


def sendUserListResponse():
    global usernameList,userList,sequenceNumReceived,userID
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
    userListResponse = struct.pack('>BBBH'+str(len(userListString))+'s', value,userID,0x01,length,userListString)
        
    return userListResponse
    
    
def sendDataMessage(payload):
    global messageType,sequenceNumSend,userID,groupID,addr_sequenceNum_ACK
    messageType = 5
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNumSend,A)    

#    payloadLength = len(pay#sequenceNumReceived =  getSequenceNumber(data)load)
#    print("payloadLength : " + str(payloadLength))
    dataMessage = struct.pack('>BBBHH' + str(len(payload)) + 's', value,userID, groupID,0x0008,len(payload),payload)
    print(dataMessage)
    
    return dataMessage
    
def updateList():
    global usernameList,userList,sequenceNumSend,messageType
    messageType = 14
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNumSend,A)
    
 
    length = len(userList) + 5
    print("usernameList : "+str(usernameList))    
    print("userList : "+str(userList))
    userListString = str(userList)
    print("userListString : "+str(userListString))
    updateList = struct.pack('>BBBH'+str(len(userListString))+'s', value,0x00,0xFF,length,userListString)
        
    return updateList
   
def groupCreationAccept():
    global sequenceNumReceived,groupPrivateList,groupID,messageType,typeServer, groupID_private,sourceID
    messageType  = 7
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNumReceived,A)
        
    typeServer = typeServer <<7
    
    print("distribuer a groupID private : "+str(groupID_private))
#    groupID = groupID + 1
#    print("groupID in group Creation Accept : "+str(groupID))
#    groupPrivateList.append(groupID)
    print("groupPrivateList in group Creation Accept : "+str(groupPrivateList))
    groupCreationAccept = ctypes.create_string_buffer(8)
    
    struct.pack_into('>BBBHBB', groupCreationAccept, 0,value,sourceID,0x00,0x0007,typeServer,groupID_private) 
    
    return groupCreationAccept

def groupCreationReject():
    global sequenceNumReceived,sourceID,messageType
    messageType  = 8
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNumReceived,A)

    groupCreationReject = ctypes.create_string_buffer(5)
    struct.pack_into('>BBBH', groupCreationReject, 0,value,sourceID,0x00,0x0005) 
    
    return  groupCreationReject

def serverTransferGroupInvitation(s,clientInvited,typeServer):
    global sequenceNumSend,userID,groupID,userList,groupID_private
    print(clientInvited)
    client_invited_list = []   
    print(len(clientInvited))
    for i in clientInvited:
        client_invited_list.append(int(i))
        
    print(client_invited_list)
    print("sequenceNumReceived in serverTransferGroupInvitation : "+str(sequenceNumReceived))
    print("userList in serverTransferGroupInvitation : "+str(userList))
    
    messageType = 0x11
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNumReceived,A)
    if typeServer == 1:
        print("group centralized")
    else :
        print("group decentralized")
        
    typeServer = typeServer <<7
    for id in client_invited_list:
        ipAddress = userList[id][2]
        print("ipAddress in serverTransferGroupInvitation : " + str(ipAddress))
        groupInvitationRequest = ctypes.create_string_buffer(9)
        struct.pack_into('>BBBHBBB', groupInvitationRequest, 0,value,userID,0x00,0x0008,typeServer,id,groupID_private)
        s.sendto(groupInvitationRequest,ipAddress)
        print("server transfered invitation success")
        print("!!!!!!!!!!!!!!!!!!!")


def groupDissolution(group_delete):
    global messageType, sequenceNumSend, groupPrivateList
    messageType = 0x0D
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNumSend,A)

    groupDissolution = ctypes.create_string_buffer(6)
    struct.pack_into('>BBBH', groupDissolution, 0,value,0x00,group_delete,0x0005)  
    return groupDissolution

def updateDisconnection(clientID_quit):
    global messageType, sequenceNumSend, userList
    messageType = 0x0F
    R = 0     
    A = 0
    value = valueControl(messageType,R,sequenceNumSend,A)
    

    updateDisconnection = ctypes.create_string_buffer(7)
    struct.pack_into('>BBBHB', updateDisconnection, 0,value,0x00,0xFF,0x0006,clientID_quit)  
    return updateDisconnection

def retransmission(s,addr,buf,messageType_ref):
    global messageType, sequenceNumReceived,ACK,resendTimeMax
    resendtime = 1
    temps_break = 1
    time.sleep(0.2)
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
            if (messageType_ref == messageType and ACK == 1):
                
                print("get response, no need to retransmission")
                temps_break = 4
                break
        if temps_break >2:
            break
        s.sendto(buf,addr)
        print("this is %s resendtime" %(resendtime-1))
        print("##############################################")
                        
                    ## wait 5s for client to reconnecter
        time.sleep(1)
        if resendtime>resendTimeMax:
            print("the last packet lost")
            return

def dataReceived(s,data,addr):
    global clientID,groupID,messageType,groupID_private,sourceID,address,userID
    global sequenceNumReceived,typeServer,resendTimeMax,sequenceNumSend
    global userList,usernameList    


    messageType = getType(data)
    print("messageType : "+ str(messageType))
    sequenceNumReceived =  getSequenceNumber(data)
    print("sequenceNumReceived : "+ str(sequenceNumReceived))
    print("sequenceNumSend : "+ str(sequenceNumSend))
    ACK = getACK(data)    
    print("ACK : "+ str(ACK)) 
#    groupID = getGroupID(data)    
#    print("groupID : "+ str(groupID))     
#    
    if (messageType == 0x00 and ACK ==0):
#   server receive client's connection, and the choose if the length is more than
#   the range of server, length of username, if existed
        print("##############################################")
        print("it is connection from client")
        username = getUsername(data)
#        print("username in 0x00: "+ str(username))
#        print("usernameList in 0x00: "+ str(usernameList))
#        print("userList length: "+ str(len(userList)))
        if len(userList) < 256:
            n = len(username)
            print("username length: "+ str(n))
            if n>8: 
                Error = 1
                print("maximum number of users exceeded")
                Reject = connectionReject(data,Error)
                s.sendto(Reject,addr)
                
                ###############retransmission
                messageType_ref = 0x02
                retransmission(s,addr,Reject,messageType_ref)

                
            else :     

                if username not in usernameList:
                    print("connection accept in server")
                    Accept = connectionAccept(data)
                    s.sendto(Accept,addr)
                    #####retransmission
                    messageType_ref = 0x01
                    retransmission(s,addr,Accept,messageType_ref)

    
                else :
                    Error = 0
                    print("uername already used")  
                    Reject = connectionReject(data,Error)
                    s.sendto(Reject,addr)
                    messageType_ref = 0x02
                    retransmission(s,addr,Reject,messageType_ref)                    

                 
        else :
            print("server is full")
            Reject = connectionReject(data,Error)
            s.sendto(Reject,addr)
            
            messageType_ref = 0x02
            retransmission(s,addr,Reject,messageType_ref)

#    elif(messageType == 0x01 and ACK==1):
#        print("##############################################")
#        print("ACK in 0x01 :"  +str(ACK))
#        print("it is connection ACK from client ")
##        sourceID = getSourceID(data)
##        print("sourceID : "+ str(sourceID))
#        
#        
#    elif(messageType == 0x02 and ACK==1):
#        print("##############################################")
#        print("ACK in 0x02 :"  +str(ACK))
#        print("it is disconnection ACK from client ")
##        sourceID = getSourceID(data)
##        print("sourceID : "+ str(sourceID))   


        
      
     
    elif (messageType == 0x03 and ACK == 0):
        print("##############################################")
        print("userList Request")

        print("clientID : "+ str(clientID))
        print("userlist sended : " + str(userList))
        userListResponse = sendUserListResponse()
        s.sendto(userListResponse,addr)
        messageType_ref = 0x04
        retransmission(s,addr,userListResponse,messageType_ref)         
        
    elif(messageType == 0x04 and ACK==1):
        print("##############################################")
        print("ACK in 0x04 :"  +str(ACK))
        print("client  has received userList respond" )        
        
#    elif (messageType == 0x05)                   clienID:
#        
#        print("transfer a message from client")
#
#        print("clientID : "+ str(clientID))
#        print("userlist sended : " + str(userList))
#        userListResponse = sendUserListResponse()
#        s.sendto(userListResponse,addr)
        
    elif (messageType == 0x05 and ACK == 0):
        print("##############################################")
        print("transfer a message from client")
        respond = acknowledgement()
        s.sendto(respond,addr)
        payload = getPayload(data)
        userID = getSourceID(data)
        dataMessage = sendDataMessage(payload)
        print("address :" +str(address))
        for i in address:
            print(addr==i)  
            if i != addr:
                
                print("addr :" +str(addr))
                print("i :" +str(i))
                s.sendto(dataMessage,i)
                time.sleep(5)
                messageType_ref = 0x05
                retransmission(s,addr,dataMessage,messageType_ref)
                
    elif (messageType == 0x05 and ACK == 1):
        print("##############################################")
        userID = getSourceID(data)
        print("transfer a message sucess of client %s"%userID)
        
        
######################################    server receives a group creation request and transfer group invitation    
    elif(messageType == 0x06):
        print("##############################################")
        print("server receives a group creation request")
        clientInvited = getClientInvited(data)
#        print("clientInvited : " + str(clientInvited))
#        print(clientInvited[0])
        print("distribuer group ID private")

        groupID_private = groupID + 1
        print("groupID_private in group Creation Accept : "+str(groupID_private))
#        groupPrivateList.append(groupID_private)
#        print("groupPrivateList in group Creation Accept : "+str(groupPrivateList))        
        
        
        typeServer = getTypeServer(data)
        if typeServer == 1:
            print("group centralized")
        else :
            print("group decentralized")
                       
        serverTransferGroupInvitation(s,clientInvited,typeServer)


######### if client has accepted invitation        
    elif(messageType == 0x0A and ACK == 0):
        print("#######################")
        print("length data" +str(len(data)))
        print("ACK in 0x0A :"  +str(ACK))
        sourceID = getSourceID(data)
        userID = getUserID(data)
        print("client %s has accepted invitation" %userID) 
        
        for i in userList:
            if i == sourceID:
                addr1 = userList[sourceID][2]

                groupCA = groupCreationAccept()
                        
                print("userList in 0x0A : " +str(userList))
                s.sendto(groupCA, addr1)        
                print("send groupCA")
            else :
                addr2 = userList[userID][2]
              
            ######### send  client invited, ACK
                print("messageType :"+str(messageType))
                respond = acknowledgement() 
                s.sendto(respond, addr2)                
                print("send invitation ACK")                   
######### send source client who demande a group requesnt, a group creation accept

    elif((messageType == 0x0A and ACK == 1) or  (messageType == 0x07 and ACK==1)):   
        print("#######################")
        print("group creation success")        
        print("userList  : " +str(userList))
        print("groupID_private : " +str(groupID_private))
        groupPrivateList [groupID_private] = [userID,sourceID]
        userList[userID][1] =  groupID_private
        userList[clientID] [1] = groupID_private 
        print("groupPrivateList" + str(groupPrivateList))
        print("new userList : " +str(userList))
      
#        print("addr1 of client1 in 0x0A :"+str(addr1))
#        addr2 = userList[2][2]
#        print("addr2 of client2 in 0x0A :"+str(addr2))
                
##########when client invited refuse the invitation                
    elif(messageType == 0x0B and ACK==0):
        print("#######################")
        print("ACK in 0x0B :"  +str(ACK))
        sourceID = getSourceID(data)
        userID = getUserID(data)
        print("client %s has refused invitation" %userID)   
        
        print("userList in 0x0A : " +str(userList))
                  
############# send source client a group creation refused        
        for i in userList:
            if i == sourceID:
                addr1 = userList[i][2]
                print("sequenceNumSend in 0x0A" + str(sequenceNumSend))
                groupCR = groupCreationReject()
                s.sendto(groupCR, addr1)

                print("send groupCR")
            else :
                #############          send client invited a ACK
                addr2 = userList[i][2]
        
                messageType = 0x0B
                respond = acknowledgement()
                s.sendto(respond, addr2)                
                print("send refused invitation ACK")              
    
                  
                
                
    elif(messageType == 0x0C and ACK==0):
        print("#######################")
        print("ACK in 0x0C :"  +str(ACK))
        userID = getSourceID(data)
        print("groupPrivateList" + str(groupPrivateList))
        print("userList : "+ str(userList))
        print("client %s leave private group and join in public" %userID)
        group_private = userList[userID][1]
        for i in range (len(groupPrivateList[group_private])):
            if groupPrivateList[group_private][i] == userID:
                temp = i
                print("temp : "+str(temp))
        del groupPrivateList[group_private][temp]
                    
        userList[userID][1] = 1
        print(" new groupPrivateList" + str(groupPrivateList))
        print("new userList : "+ str(userList))


    elif(messageType == 0x0E and ACK==1):
        print("#######################")
        print("ACK in 0x0C :"  +str(ACK))

        print("client update list success" )


    elif(messageType == 0x10):
        if ACK == 0:
            print("##############################################")
            print("it is disconnection request")
#        sourceID = getSourceID(data)
#        print("sourceID : "+ str(sourceID))

            respond = acknowledgement()
            s.sendto(respond,addr)
        else :
            print("disconnection ACK from client %s"%clientID)       
    
#    elif(messageType == 0x11 ):
#        print("#######################")
#        print("get transfered invitation success")     
       
        

        

        

#        print("clientID : "+ str(clientID))
#        print("groupID : "+ str(groupID)) 



    


#userList[username] = [ip, port, clientID,groupID] 




#print(str(readable) + '\n')

#print(str(inputs) + '\n')
inputs = [s, sys.stdin]
while True : 
    readable,writable,exceptional = select.select(inputs,[],[])    
    for r in readable:	
        if s==r:
            data,addr = s.recvfrom(1024)

#            print (data)

            #print(str(data) + '\n')
            if addr not in address:
                address.append(addr)
                print("address in main :" +str(address))
            if data !="end":
                print ('connected by',addr)
                dataReceived(s,data,addr)

                #print(str(inputs) + '\n')
            else:
                address.remove(addr)
                if len(address)==0:
                    s.close()
                    sys.exit()
                    
        else :
            print("##############################################")
            print ("chose type to do")
            mType = sys.stdin.readline().strip()
            
            if (mType == 'dissolution'):
                sequenceNumSend = (sequenceNumSend + 1)%2
                print("groupPrivateList : " +str(groupPrivateList))
                print("userList : " +str(userList))  
#                group_delete = []
                for i in groupPrivateList:
                    n = len(groupPrivateList[i])
                    print("n in dissolution : " +str(n))
                    if n ==1:
#                        group_delete.append[i]
                        client_rest = groupPrivateList.pop(i)
                        print("client_rest :" +str(client_rest) )
                        ipAdrr_rest = userList[client_rest[0]][2]
                        print("ipAdrr_rest :" +str(ipAdrr_rest) )
                        groupD = groupDissolution(i)

                    if n == 0:
#                         group_delete.append[i]
                        groupPrivateList.clear()
                s.sendto(groupD,ipAdrr_rest)
                print("send dissolution") 
#                print("group_delete : "+str(group_delete))
                
            if (mType == 'updateList'):
                sequenceNumSend = (sequenceNumSend + 1)%2
                print("groupPrivateList : " +str(groupPrivateList))
                print("userList : " +str(userList))  
#                group_delete = []
                updateList = updateList()
                for i in address:
                    s.sendto(updateList,i) 
               
                print("send updateList")
                
            if (mType == 'updateDisconnection'):
                sequenceNumSend = (sequenceNumSend + 1)%2
                print("input clientID who leave the system")
                print("old userList : " +str(userList))  
                clientID_quit = raw_input()
                clientID_quit = int(clientID_quit)
                print("groupPrivateList : " +str(groupPrivateList))
                del userList[clientID_quit]
                print("new userList : " +str(userList))  
#                group_delete = []
                updateDisconnection = updateDisconnection(clientID_quit)
                
                for i in address:
                    s.sendto(updateDisconnection,i) 
               
                print("send updateDisconnection")
                                

                        
                        
                        
                        
                        
                        
                        
                        
                        
                        