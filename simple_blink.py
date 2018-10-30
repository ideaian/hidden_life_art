import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
#GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ledPin = 11

GPIO.setup(ledPin, GPIO.OUT)
timeout = 0.5 
for i in range(50000):
	print("LED turning on.")
	GPIO.output(ledPin, GPIO.HIGH)
	time.sleep(timeout)
	print("LED turning off.")
	GPIO.output(ledPin, GPIO.LOW) 
        time.sleep(timeout)
