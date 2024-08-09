#!/usr/bin/env python

import RPi.GPIO as GPIO
import I2C_LCD_driver
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
import requests
import json
from servo_driver import *
from mfrc522 import SimpleMFRC522
from datetime import datetime
from time import sleep

# GPIO.setmode(GPIO.BOARD)
reader = SimpleMFRC522()
lcd = I2C_LCD_driver.lcd()
RELAY_PIN = 12

# for LEDs
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

# Set the relay pin as an output pin
GPIO.setup(RELAY_PIN, GPIO.OUT)


# List of users with access
id_name_mapping = {
    "609170465688": "Vlad",
    "634260097519": "Alex",
    "769282541687": "Alice",
    "495547714024": "Bob",
    
    # Add more ID to Name mappings here
}

server_address = 'http://10.0.1.91:5000'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}



def send_post_to_server(json_text):
    requests.post(server_address, data=json_text, headers=headers)


def display_waiting_text():
    lcd.lcd_display_string("Waiting for card")
    lcd.lcd_clear()

    lcd.lcd_display_string("Waiting for card.")
    sleep(0.5)
    lcd.lcd_clear()

    lcd.lcd_display_string("Waiting for card..")
    sleep(0.5)
    lcd.lcd_clear()

    lcd.lcd_display_string("Waiting for card...")
    sleep(0.5)


def read():
    global id
    global text

    t = threading.Thread(target=display_waiting_text)
    t.start()

    id, text = reader.read()
    t.join()

    print(id)
    print(text)

    if str(id) in id_name_mapping:
        name = id_name_mapping[str(id)]
        GPIO.output(13, GPIO.HIGH)

        lcd.lcd_display_string("Access granted: " + name, 1)
        json_text = json.dumps({"name": name, "time": str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")), "status": "granted"})
        t1 = threading.Thread(target=send_post_to_server, args=(json_text,))
        t1.start()
        
        # servo.unlock()
        # Turn the relay OFF (LOW) to unlock the door
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        sleep(5)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(RELAY_PIN, GPIO.LOW)
        sleep(5)
        # servo.lock()
    else:
        print(text)
        GPIO.output(11, GPIO.HIGH)
        lcd.lcd_display_string("Access denied: " + text, 1)
        json_text = json.dumps({"name": str(id), "time": str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")), "status": "denied"})
        t1 = threading.Thread(target=send_post_to_server, args=(json_text,))
        t1.start()
        
        sleep(3)
        GPIO.output(11, GPIO.LOW)

    id = 0
    text = ""
    # GPIO.cleanup()


if __name__ == "__main__":
    try:
        while True:
            read()
    finally:
        GPIO.cleanup()
