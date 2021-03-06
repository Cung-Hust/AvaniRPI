#!/usr/bin/python3
 
import time
import serial
import threading

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for i in range(1, 14):
    # s = "GPIO.setup(" + str(i) + ", GPIO.OUT)"
    s = GPIO.setup(i, GPIO.OUT)
    # print(s)
    GPIO.output(i, GPIO.HIGH)
for i in range(16, 28):
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, 1)

ser = serial.Serial(
	port = '/dev/ttyS0',
	baudrate = 115200,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 0.1
)
 
print("Raspberry's receiving : ")

def device():
    while True:
        s = ser.readline()
        data = s.decode()			# decode s
        data = data.rstrip()			# cut "\r\n" at last of string
        if(data):
            print(data)				# print string
try:
    t0 = threading.Thread(target=device, args=())
    t0.start()
    t0.join()
 
except KeyboardInterrupt:
	ser.close()