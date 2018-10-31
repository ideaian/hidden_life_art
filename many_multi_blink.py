import RPi.GPIO as GPIO
import time
from collections import namedtuple
import numpy as np
#:wGPIO.setwarnings(False)
'''
#: Previous way of doing it
GPIO.setmode(GPIO.BOARD)
color_pin_dict = {
        'blue': 11,
        'red': 15,
        'green': 18,
        }

StrandPids = namedtuple("StrandPids",'r','g','b','mode')
time_on = 2.0
for key, ledPin in color_pin_dict.iteritems():
    GPIO.setup(ledPin, GPIO.OUT)

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
'''
PINOUT_MATRIX = \
        np.array([[23, 12, 21],
                  [24, 25, 26],
                  [26, 13, 4],
                  [17, 22, 5]
                  ], dtype=int)


def main():
    GPIO.setmode(GPIO.BCM)

    zero_intensity_matrix = GPIO.LOW * np.ones(shape=PINOUT_MATRIX.shape, dtype=int)
    all_intensity_matrix = GPIO.HIGH * np.ones(shape=PINOUT_MATRIX.shape, dtype=int)


    init_gpio_pins()
    time_on = 0.001
    time_off = 0.001

    try:
        while True:
            update_lights(all_intensity_matrix)
            time.sleep(time_on)
            update_lights( zero_intensity_matrix)
            time.sleep(time_off)

    except KeyboardInterrupt:
        print("Exiting")
    finally:
        print("Cleaning up")
        update_lights(zero_intensity_matrix)    
        update_lights(zero_intensity_matrix)    
        GPIO.cleanup()


def update_string(pinout_array, intensity_array, changed_state=True):
    if not changed_state:
        return
    for pin, intensity in zip(pinout_array, intensity_array):
        GPIO.output(pin, intensity)

def update_lights(intensity_matrix, changed_state=True):
    if not changed_state:
        return
    for (pin, intensity) in zip(PINOUT_MATRIX, intensity_matrix):
        update_string(pin, intensity)

def init_gpio_pins():
    for pin in iter(PINOUT_MATRIX.flat):
        GPIO.setup(pin, GPIO.OUT)

def make_color_matrix(n_lights, color):

    out_matrix = np.ones(shape=(n_lights, 3), dtype=int) * GPIO.LOW
    for i in range(n_lights):
        out_matrix[i, color] = GPIO.HIGH

    return out_matrix


if __name__ == '__main__':
    main()
