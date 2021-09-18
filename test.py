#!/usr/bin/env python
# ls -l /dev/hidraw* : check list hidraw
import pika
import json
import _thread
import os
import sys
from datetime import datetime
import time
import serial
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

from pika.connection import Connection

os.system('sudo chmod 666 /dev/hidraw0')
os.system('sudo chmod 666 /dev/hidraw1')
os.system('sudo chmod 666 /dev/ttyS0')

# config RPI
for i in range(1, 14):
    # s = "GPIO.setup(" + str(i) + ", GPIO.OUT)"
    s = GPIO.setup(i, GPIO.OUT)
    # print(s)
    GPIO.output(i, GPIO.HIGH)
for i in range(16, 28):
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, 1)

# ser = serial.Serial(
# 	port = '/dev/ttyS0',
# 	baudrate = 115200,
# 	parity = serial.PARITY_NONE,
# 	stopbits = serial.STOPBITS_ONE,
# 	bytesize = serial.EIGHTBITS,
# 	timeout = 0
# )

# #################################
# connect rabbitMQ

# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(
#         '192.168.1.12', 5672,
#         pika.PlainCredentials('guest', 'guest'),
#         blocked_connection_timeout=1000,
#         heartbeat=0,))

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        '192.168.1.9', 5672, 
        '/', 
        pika.PlainCredentials('avani', 'avani'),
        blocked_connection_timeout=1000,
        heartbeat=0,))
channel = connection.channel()

# channel.queue_declare(queue='rfid')
# channel.queue_declare(queue='barcode')

channel.queue_declare(queue='test')

# # ============== - RFID - ==============


# def rfid_read(fp):
#     while True:
#         fp.flush()
#         code = fp.read(64)
#         tag = code.hex()
#         # rfid_mess = 'RFID-TAG:' + tag[38:42]
#         rfid_mess = {
#             "type": "rfid",
#             "time": datetime.now().strftime('%Y%m%d%H%M%S'),
#             "data": tag[38:42]
#         }

#         rf_msg = json.dumps(rfid_mess)

#         channel.basic_publish(
#             exchange='', routing_key='test', body=rf_msg)
#         print(rfid_mess)

# # ============== - BARCODE - ==============


# def filter(input):
#     b = ''
#     for c in input:
#         if c.isprintable():
#             b = b + str(c)
#     return b


# def scanner(fp):
#     while True:
#         fp.flush()
#         code = fp.read(64)
#         bar_mess = 'BARCODE:' + filter(code.decode())
#         bar_mess = {
#             "type": "barcode",
#             "time": datetime.now().strftime('%Y%m%d%H%M%S'),
#             "data": filter(code.decode())
#         }

#         ba_msg = json.dumps(bar_mess)

#         channel.basic_publish(
#             exchange='', routing_key='test', body=ba_msg)
#         print(bar_mess)

# ============== - DEVICE - ==============

def device(ser):
    try:
        while True:
            s = ser.readline()
            data = s.decode()			# decode s
            data = data.rstrip()			# cut "\r\n" at last of string
            if(data):
                # print(data)			# print string
                dev_mess = {
                    "type": "device",
                    "time": datetime.now().strftime('%Y%m%d%H%M%S'),
                    "data": data
                }

                dev_msg = json.dumps(dev_mess)

                channel.basic_publish(
                    exchange='', routing_key='test', body=dev_msg)
                print(dev_mess)
 
    except KeyboardInterrupt:
        ser.close()

try:
    ser = serial.Serial(ort = '/dev/ttyS0', baudrate = 115200, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, timeout = 0)
    _thread.start_new_thread(device, ser)
except:
    # print("error!")
    connection.close()

while True:
    pass
