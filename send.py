#!/usr/bin/python3
 
import time
import serial
import _thread
 
ser = serial.Serial(
	port = '/dev/ttyS0',
	baudrate = 115200,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)
 
print("Raspberry's sending : ")
i = 0
try:
    while True:
    	ser.write(b'hi')
    	ser.flush()
    	print("he")
    	time.sleep(1)
except KeyboardInterrupt:
	ser.close()