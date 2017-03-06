import socket
import sys,os
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
        struct.pack_into('bbbH8s', connect, 0,0x00,0x00,0x00,0x0000,str(username).encode('UTF-8'))
        s.sendto(connect,addr)
            
    else:
        print("nom is over the length")
    

    

    
    
    
PORT = 1248
HOST = 'localhost'
addr = (HOST,PORT)
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect((HOST,PORT))

childPid = os.fork()


if childPid ==0:
    while True:
        mes,addr1 = s.recvfrom(1024)
        
        print(mes)
    
else:
    

    while True:
        print("are you want to connect, please input your name")
        username = raw_input()
        if len(username) <=8:
            n = len(username)
            username = username + (8-n)*'0'
            connect = ctypes.create_string_buffer(14)
            #put data into the buffer
            struct.pack_into('bbbH8s', connect, 0,0x00,0x00,0x00,0x0000,str(username).encode('UTF-8'))
            s.sendto(connect,addr)
            
        else:
            print("nom is over the length")
            
            
            
            
            
            
            
            
            
            