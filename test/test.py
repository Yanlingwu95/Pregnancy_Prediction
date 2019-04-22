import RPi.GPIO as GPIO
import time
import os
import threading as th
import multiprocessing 
from multiprocessing import pool
from multiprocessing import Process

GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)

GPIO.output(16,0)
GPIO.output(17,0)

def templed(tem1):
	th.Timer(5,exit2).start()
    count=0
    if tem1=="Tup":
        while count<10:
            GPIO.output(16,1)
            time.sleep(0.3)
            GPIO.output(16,0)
            time.sleep(0.3)
    elif tem1=="Tdown":
        while count<10:
            GPIO.output(16,1)
            time.sleep(0.3)
            time.sleep(0.3)
    else:
        while count<10:
            time.sleep(0.3)
            time.sleep(0.3)

def humled(tem2):
	th.Timer(5,exit2).start()
    count=0
    if tem2=="Hup":
        while count<10:
            GPIO.output(17,1)
            time.sleep(0.3)
            GPIO.output(17,0)
            time.sleep(0.3)
    elif tem2=="Hdown":
        while count<10:
            GPIO.output(17,1)
            time.sleep(0.3)
            time.sleep(0.3)
    else:
        while count<10:
            time.sleep(0.3)
            time.sleep(0.3)
            

def moisled(tem3):
	th.Timer(5,exit2).start()
    count=0
    if tem3=="Mup":
        while count<10:
            GPIO.output(5,1)
            time.sleep(0.3)
            GPIO.output(5,0)
            time.sleep(0.3)
    elif tem3=="Mdown":
        while count<10:
            GPIO.output(5,1)
            time.sleep(0.3)
            time.sleep(0.3)
    else:
        while count<10:
            time.sleep(0.3)
            time.sleep(0.3)
            

def ligled(tem4):
    count=0
    if tem4=="Lup":
        while count<10:
            GPIO.output(6,1)
            time.sleep(0.3)
            GPIO.output(6,0)
            time.sleep(0.3)
    elif tem4=="Ldown":
        while count<10:
            GPIO.output(6,1)
            time.sleep(0.3)
            time.sleep(0.3)
    else:
        while count<10:
            time.sleep(0.3)
            time.sleep(0.3)
response = ""
error = False
    
TEMP=""
HUM=""
MOIS=""
LIG=""
methods=["Tup","Hup"]
if methods[0] == "Tup":
    print("Temperature up")
    TEMP='Tup'
    response += "Temperature up, "
elif methods[0] == "Tdown":
    print("Temperature down")
    TEMP='Tdown'
    response += "Temperature down"
elif methods[0] == "Tst":
    print("Temperature stay")
    TEMP="Tstay"
    response += "Temperature stay"
else:
    print("Error! Temperature method name is wrong!")
    error = True
        
if methods[1] == "Hup":
    print("Humidity up")
    HUM='Hup'
    response += "Humidity up, "
elif methods[1] == "Hdown":
    print("Humidity down")
    HUM='Hdown'
    response += "Humidity down, "
elif methods[1] == "Hst":
    print("Humidity stay")
    HUM="Hstay"
    response += "Humidity stay, "
else:
    print("Error! Humidity method name is wrong!")
    error = True
        


print (type(TEMP),HUM)
p1=Process(target=templed,args=(TEMP,))
p2=Process(target=humled,args=(HUM,))

p1.start()
p2.start()

p1.join()
p2.join()

    
GPIO.cleanup()
