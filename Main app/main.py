import RPi.GPIO as GPIO
import threading
import read
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

while(True):
    try:
        read.read()
    finally:
        pass




				
				
