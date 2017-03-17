import ctypes
import struct
import argparse


##Sender
#buf = ctypes.create_string_buffer(7)
## put data into the buffer
#struct.pack_into('>B3sBH', buf, 0, 0b00000010, b'abc', 2, 455)
#
##receiver
#premier=struct.unpack('B', buf[0])
#print ("Premier element : " + str(premier[0]))
#print ("Premier element en binaire : " + str(bin(premier[0])))
#
#chaine = struct.unpack('3s', buf[1:4])
#print ("Voici la chaine de caracteres : " + chaine[0].decode('UTF-8'))
#
#
##Ici vous pouvez afficher le chiffre 10 en decimal et en binaire
#dernier = struct.unpack_from('B', buf, 4)
#print (dernier[0])
#
#big = struct.unpack_from('>H', buf, 5)
#print (big[0])
#
#chaine2 = struct.unpack('>B3sBH', buf)
#print (chaine2)
#username = 'haha'
#x = {}.fromkeys([username])
#x[username ] = ['fuck','wocao']
#clientID = x[username][0]
#print(x)
#print(len(x))
#x[username] = [ip,port,clientID,groupID]
#x = 1
#x = (x +1)%2
#print(x)


import os
from multiprocessing import Queue,Process
import time

Qmsg = Queue()

pid = os.fork()
if(pid ==0 ):
    msg = Qmsg.get()
    print( msg)
    msg = Qmsg.get()
    print( msg)

else:
    Qmsg.put('hello')
    Qmsg.put([1,2,3,4])
    os.wait