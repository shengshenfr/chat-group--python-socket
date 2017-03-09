# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""



import ctypes
import struct
import argparse


#print("please distribuer client ID")
#ID = raw_input()
#if len(ID) <= 8:
#    n = len(ID)
#    ID =  (8-n)*'0'+ ID
#    print ("ID"+str(ID))
#    
#Accept = ctypes.create_string_buffer(14)
#struct.pack_into('bbbH8s', Accept, 0,0b00001000,0x00,0x00,0x0000,str(ID).encode('UTF-8'))
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
buf = ctypes.create_string_buffer(7)
# put data into the buffer
struct.pack_into('>B3sBH', buf, 0, 0b00011011, b'abc', 2, 455)
premier=struct.unpack('B', buf[0])
print ("Premier element : " + str(premier[0]))
print ("Premier element en binaire : " + str(bin(premier[0])))
type1 = bin(premier[0]>>3)
print("type1:"+str(type1))
S = str(bin(premier[0]))
print("S:"+S)
n = len(S)
print("n:"+str(n))
R1 = S[n-3]
print("R1:"+R1)
senquenceNum = S[n-2]
print("senquenceNum:"+senquenceNum)

A = S[n-1]
print("ACK:"+A)



Error = 1
e = str(Error)
print(e)
e = e+ 7*'0'
print(e)

