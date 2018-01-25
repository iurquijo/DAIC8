#!/usr/bin/env python
#LUZPOSICION.PY


import RPi.GPIO as GPIO, time, os, sys     

#Settings
IN_RC= 18       #Input pin
OUT_LOW = 24    #Baja luminosidad output
OUT_HIGH = 25   #Alta luminosidad output
OUT_STATE = 22  #Estado del programa output


DEBUG = 1
GPIO.setmode(GPIO.BCM)

GPIO.setup(OUT_LOW, GPIO.OUT)
GPIO.setup(OUT_HIGH, GPIO.OUT)
GPIO.setup(OUT_STATE, GPIO.OUT)

def RCtime (RCpin):
        reading = 0
        GPIO.setup(RCpin, GPIO.OUT)
        GPIO.output(RCpin, GPIO.LOW)
        time.sleep(0.1)

        GPIO.setup(RCpin, GPIO.IN)
        # 1 ms por ciclo del loop
        while (GPIO.input(RCpin) == GPIO.LOW):
                reading += 1
        return reading

def ledOut(state):
    if state == 0:
        GPIO.output(OUT_LOW, True)
        GPIO.output(OUT_HIGH, True)
        return 0
    if state == 1:
        GPIO.output(OUT_LOW, False)
        GPIO.output(OUT_HIGH, True)
        return 0
    if state == 2:
        GPIO.output(OUT_LOW, True)
        GPIO.output(OUT_HIGH, False)
        return 0
    if state == 3:
        GPIO.output(OUT_LOW, False)
        GPIO.output(OUT_HIGH, False)
        return 0
    return 1

def photocellParse(reading):
    out = " "
    if reading <= 100: #LUMINOSIDAD MUY ALTA, SE ENCIENDEN LAS DOS
        out = "0"
        ledOut(0)
        return out
    if reading <= 250: #LUMINOSIDAD MODERADA
        out = "o"
        ledOut(1)
        return out
    if reading <= 2000: #LUMINOSIDAD BAJA
        out = "."
        ledOut(2)
        return out
    out = " "
    ledOut(3)
    return out


while True:
        GPIO.output(OUT_STATE, True)
        sys.stdout.write(photocellParse(RCtime(IN_RC)))    
        sys.stdout.flush()
        GPIO.output(OUT_STATE, False)
