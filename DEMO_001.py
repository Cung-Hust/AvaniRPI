import threading
import time
from datetime import datetime
import json
import os
import pika
import serial


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for i in range(1, 14):
    s = GPIO.setup(i, GPIO.OUT)
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

# ########################################
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

#  READ _ DEVICE #########################

def device():
    while True:
        s = ser.readline()
        data = s.decode()			# decode s
        data = data.rstrip()			# cut "\r\n" at last of string
        if(data):
            print(data)				# print string

# ########################################

def filter(input):
    b = ''
    for c in input:
        if c.isprintable():
            b = b + str(c)
    return b

def read(f_name):
    while True:
        try:
            os.system('sudo chmod 666 /dev/hidraw*')
            fp = open(f_name, 'rb')
            try:
                print("READING...")
                code = fp.read(64)
                fp.close()
                try:
                    bar_mess = 'BARCODE:' + filter(code.decode())
                    print(bar_mess)
                    bar_mess = {
                        "type": "barcode",
                        "time": datetime.now().strftime('%Y%m%d%H%M%S'),
                        "data": filter(code.decode())
                    }

                    bar_msg = json.dumps(bar_mess)

                    channel.basic_publish(
                        exchange='', routing_key='test', body=bar_msg)
                    print(bar_msg)
                    
                except:
                    tag = code.hex()
                    print("rfid:" + tag[38:42])
                    rfid_mess = {
                        "type": "rfid",
                        "time": datetime.now().strftime('%Y%m%d%H%M%S'),
                        "data": tag[38:42]
                    }

                    rfid_msg = json.dumps(rfid_mess)

                    channel.basic_publish(
                        exchange='', routing_key='test', body=rfid_msg)
                    print(rfid_msg)
            except:
                print("close")
                fp.close()  
        except:
            time.sleep(1)
            pass


try:

    t0 = threading.Thread(target=read, args=("/dev/hidraw0",))
    t1 = threading.Thread(target=read, args=("/dev/hidraw1",))
    t2 = threading.Thread(target=read, args=("/dev/hidraw2",))
    t3 = threading.Thread(target=device, args=())
    
    t0.start()
    t1.start()
    t2.start()
    t3.start()

    t0.join()
    t1.join()
    t2.join()
    t3.join()

except:
    print ("error")