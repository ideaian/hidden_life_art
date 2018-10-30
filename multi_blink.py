import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
#GPIO.setmode(GPIO.BCM)
#:wGPIO.setwarnings(False)


color_pin_dict = {
        'blue': 11,
        'red': 15,
        'green': 18,
        }

for key, ledPin in color_pin_dict.iteritems():
    GPIO.setup(ledPin, GPIO.OUT)
time_off = 0.5 
time_on = 2.0
try:
    for i in range(50000):
        for key, ledPin in color_pin_dict.iteritems():
            print("{} LED turning on.".format(key))
            GPIO.output(ledPin, GPIO.HIGH)
            time.sleep(time_on)
            print("{} LED turning off.".format(key))
            GPIO.output(ledPin, GPIO.LOW) 
            time.sleep(time_off)
except:
    print("exit")
finally:
    print("Cleanup")
    GPIO.cleanup()
