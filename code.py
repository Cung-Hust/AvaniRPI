#!/usr/bin/env python
# ls -l /dev/hidraw* : check list hidraw
import pika
import json
import _thread
import os
import sys
from datetime import datetime
import time


from pika.connection import Connection

os.system('sudo chmod 666 /dev/hidraw0')
os.system('sudo chmod 666 /dev/hidraw1')
# #################################
# connect rabbitMQ

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        '192.168.0.104', 5672, 
        '/', 
        pika.PlainCredentials('avani', 'avani'),
        blocked_connection_timeout=1000,
        heartbeat=0,))
channel = connection.channel()
channel.queue_declare(queue='test')

# ============== - RFID - ==============


def rfid_read(fp):
    while True:
        fp.flush()
        code = fp.read(64)
        tag = code.hex()
        # rfid_mess = 'RFID-TAG:' + tag[38:42]
        rfid_mess = {
            "type": "rfid",
            "time": datetime.now().strftime('%Y%m%d%H%M%S'),
            "data": tag[38:42]
        }

        rf_msg = json.dumps(rfid_mess)

        channel.basic_publish(
            exchange='', routing_key='test', body=rf_msg)
        print(rfid_mess)

# ============== - BARCODE - ==============


def filter(input):
    b = ''
    for c in input:
        if c.isprintable():
            b = b + str(c)
    return b


def scanner(fp):
    while True:
        fp.flush()
        code = fp.read(64)
        bar_mess = 'BARCODE:' + filter(code.decode())
        bar_mess = {
            "type": "barcode",
            "time": datetime.now().strftime('%Y%m%d%H%M%S'),
            "data": filter(code.decode())
        }

        ba_msg = json.dumps(bar_mess)

        channel.basic_publish(
            exchange='', routing_key='test', body=ba_msg)
        print(bar_mess)

try:
    f0 = open('/dev/hidraw0', 'rb')
    f1 = open('/dev/hidraw1', 'rb')
    _thread.start_new_thread(rfid_read, (f1,))
    _thread.start_new_thread(scanner, (f0,))
except:
    print("error!")
    connection.close()

while True:
    pass
