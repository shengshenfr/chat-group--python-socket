# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""



import ctypes
import struct
import argparse


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

#type =3
#R = 0
#S = 1
#ACK = 0
#value = type    
##    print(bin(value))
#value = value + R <<1
##    print(value)
#value = value + S <<1 
#value = value + ACK <<1  
#
#
#disconnectionRequest = ctypes.create_string_buffer(5)
#struct.pack_into('>BBBH', disconnectionRequest, 0,value,0x01,0x01,0x0006)
#premier=struct.unpack('b', disconnectionRequest[0])
#print(len(disconnectionRequest))
#print ("Premier element : " + str(premier[0]))
#print ("Premier element en binaire : " + str(bin(premier[0])))
  
#userListRequest = ctypes.create_string_buffer(12)
#struct.pack_into('b8sbH', userListRequest, 0,value,ID,0x01,0x0006)
#
#    
#premier=struct.unpack('b', userListRequest[0])
#print ("Premier element : " + str(premier[0]))
#print ("Premier element en binaire : " + str(bin(premier[0])))
#
#groupID = struct.unpack_from('b', userListRequest,9) #offset = 0
##the content of buf is a group of 4 elements: control, real msg length, seq num, real msg
#
#print(groupID)

#print("please input payload")
#    
#payload = raw_input()
#print("payload : " + str(payload))
#
#
#payloadLength = len(payload)
#print("payloadLength : " + str(payloadLength))
#dataMessage = struct.pack('>BBBHH' + str(len(payload)) + 's', value, 0x00, 0x00,0x0008,len(payload),payload)
##dataMessage = ctypes.create_string_buffer(12)
##struct.pack_into('b8sbHHb', dataMessage, 0,value,ID,0x01,0x0008,payloadLength,payload_hex)  
#
#print(dataMessage)
#premier=struct.unpack('B', dataMessage[0])
#print ("Premier element : " + str(premier[0]))
#print ("Premier element en binaire : " + str(bin(premier[0])))
#
#bufFormat= '>BBBHH' + str(len(dataMessage) - 7) + 's'
#getPayload = ctypes.create_string_buffer(len(dataMessage))
#getPayload = struct.unpack_from(bufFormat, dataMessage, 0)
#
#payload = getPayload[5]
#print("payload : " + str(payload))



#print("are you want to connect, please input your name")
#username = raw_input()
#if len(username) <=8:
#    n = len(username)
#    username = username + (8-n)*'0'
#    print("username:"+str(username))
#    connect = ctypes.create_string_buffer(14)
#    #put data into the buffer
#    struct.pack_into('BBBH8s', connect, 0,0x00,0x00,0x00,0x0000,str(username).encode('UTF-8'))
#
##receiver
#premier=struct.unpack('B', connect[0])
#print ("Premier element : " + str(premier[0]))
#print ("Premier element en binaire : " + str(bin(premier[0])))
#chaine = struct.unpack('8s', connect[1:9])
#print ("Voici la chaine de caracteres : " + chaine[0].decode('UTF-8'))
#username = chaine[0].decode('UTF-8')
#print(username)

#type = 2
#R= 0
#sq = 1
#ACK = 1
#value = type
#print(hex(value))
#value = value+ R <<1
#print(bin(value))
#
#value = value + sq <<1 
#value = value + ACK <<1 
#print(bin(value))



#buf = ctypes.create_string_buffer(7)
## put data into the buffer
#struct.pack_into('>B3sBH', buf, 0, 0b00011011, b'abc', 2, 455)
#premier=struct.unpack('B', buf[0])
#print ("Premier element : " + str(premier[0]))
#print ("Premier element en binaire : " + str(bin(premier[0])))
#type1 = bin(premier[0]>>3)
#print("type1:"+str(type1))
#S = str(bin(premier[0]))
#print("S:"+S)
#n = len(S)
#print("n:"+str(n))
#R1 = S[n-3]
#print("R1:"+R1)
#senquenceNum = S[n-2]
#print("senquenceNum:"+senquenceNum)
#
#A = S[n-1]
#print("ACK:"+A)
#
#
#
#Error = 1
#e = str(Error)
#print(e)
#e = e+ 7*'0'
#print(e)