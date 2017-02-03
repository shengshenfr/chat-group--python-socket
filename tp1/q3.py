'''q3
print ("I am a double quoted string")


print ("Hello " + "World !")
print ("Hello World !" * 5)
print (len ("Hello World !"))

question = "What did you have for lunch ?"
print (question)
answer = raw_input()
print (answer)

'''
'''
print ("Please give me a number :")
answer = raw_input()
number = 10 + int(answer)
print ("If we add 10 to your number, we get " + str(number))
'''

'''q4

print ("Please input a string :")
string1 = raw_input()
print (len (string1))

print ("Please give me a number :")
num1 = raw_input()
print (num1)
print (string1*int(num1))

'''
'''q5


name = raw_input("What is your name ? ")
password = raw_input("What is the password ? ")

if name == "Josh" and password == "Friday" :
    print ("Welcome Josh !")
elif name == "Fred" and password == "Rock" :
    print ("Welcome Fred !")
else :
    print ("I don''t know you")
    
    
'''
'''q4.1


import random

number = random.randint(0,10)
print(number)
num = raw_input("input un nombre ")
print(num)
if int(num) == number:
    print("win")
else :
    print("lose")

'''


'''q5.1

a=0
while a < 10 :
    a += 1
    print (a)
print ("The final value of a is " + str(a))


'''
'''q5.2

sum = 0
for item in range(0,10) :
    sum += 1
    print (sum)
print ("The final value of a is " + str(sum))

sum = 0
for item in range(10, 0, -1) :
    sum += 1
    print(item)
    print (sum)
print ("The final value of a is " + str(sum))

'''



'''q5.4 fibonacci

a = 1
b = 1
n = 10
print(a)
print(b)
while(n):
    
    a,b,n = b,a+b,n-1
    print(b)
'''

'''q5.4-3

sum = 0
string1 = raw_input("do you want to quit,if please input quit ")
s = quit
if(s != string1):
    for i in xrange(0,100):
        sum +=i
    moy = sum/i
    print(moy)
else:
    print ("quit")
'''    
    
    
'''q6.1

print("Hello, world !"[0])
"Hello, world !"[1]
"Hello, world !"[2]
"Hello, world !"[3]



print("Hello, world !"[-2])

print("Hello, world !"[3 :9])
string = "Hello, world !"
print(string[ :5])
string[-6 :-1]
print(string[-9 :])
print(string[ :])

'''
'''
spam = ["bacon", "eggs", 42]

print(spam)
print(spam[0])
print(spam[-2])
print(spam[1 :2])

print(len(spam))
spam[1] = "ketchup"
print(spam)

spam.append(10)
print(spam)

spam.insert(1, "and")
print(spam)

a = [1, 2, 3]
b=a
print a
print b
del a[2]
print a
print b
'''
'''6.3

unchanging = "rocks", 0, "the universe"
print(unchanging)

foo, bar = "rocks", (0, "the universe")
print foo
print bar

'''

'''6.4

definitions = {"guava" : "a tropical fruit", "python" : "a programming language"}
print definitions
print definitions["python"]
print len(definitions)

definitions["new key"] = "new value"
print definitions
definitions["animal"] = "cat"
print definitions

d2 = {"animal" : "loup"}
definitions.update(d2)
print definitions

d3 = {"animal" : ("loup", 2)}
definitions.update(d3)
print definitions
print definitions["animal"][0]
print definitions["animal"][1]

'''


'''q8.1

import random


s = []
for i in range(0,5):
    a = random.randint(0,100)
    s.append(a)
print("s  "+str(s))

s1 = sorted(s)
print("s1  "+str(s1))

s1.append(99)
print("nouveau s1   "+str(s1))

b = random.randint(0,100)
print ("b  "+str(b))
s1.append(b)
s2 = sorted(s1)
print("s2  "+str(s2))

print(s2[2:])
'''



'''q8.2

import random

def pile(s):

    for i in range(0,5):
        a = random.randint(0,10)
        s.append(a)
    print("s  "+str(s))


def empile(s):
    b = random.randint(0,100)
    s.append(b)
    print("s  "+str(s))

def depile(s):
    s.pop();
    print("s  "+str(s))
    
    
s = []
pile(s)
empile(s)
depile(s)

'''

'''q9

import sys
for arg in sys.argv :
    
    print arg



import sys, getopt
try :
    opts, args = getopt.getopt(sys.argv[1 :], "hf :s", ["help", "first="])
except getopt.GetoptError as err :
    print "not properly used - print the options"
    sys.exit(2)
for opt, arg in opts :
    if opt in ("-h", "--help") :
        print arg
        sys.exit()

'''
#!/usr/bin/env python  
      
import sys  
import getopt  
      


