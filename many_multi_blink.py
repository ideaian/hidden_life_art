import RPi.GPIO as GPIO
import time
from collections import namedtuple
import numpy as np
import threading

#:wGPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)
PINOUT_MATRIX = \
        np.array([[25, 24, 23],
                  [16, 21, 20],
                  [13, 19, 26],
                  [17, 22, 27]
                  ], dtype=int)
zero_intensity_matrix = GPIO.LOW * np.ones(shape=PINOUT_MATRIX.shape, dtype=int)
all_intensity_matrix = GPIO.HIGH * np.ones(shape=PINOUT_MATRIX.shape, dtype=int)

COLOR_MAP = {'r':0, 'g':1, 'b':2}

def main():
    GPIO.setmode(GPIO.BCM)
    init_gpio_pins()

    try:
       # color_test_thread()
       color_mat = make_color_matrix('r')
       simple_test(color_matrix=color_mat)
    except (KeyboardInterrupt, SystemExit):
        print("Exiting")
    finally:
        print("Cleaning up")
        update_lights(zero_intensity_matrix)    
        update_lights(zero_intensity_matrix)    
        GPIO.cleanup()

#Needs: GUI support for color choosing. 
def color_test(pin, frequency, speed, step):
    p = GPIO.PWM(pin, frequency)
    p.start(0)
    while True:
        try:
            for duty_cycle in range(0, 101, step):
                p.ChangeDutyCycle(duty_cycle)
                time.sleep(speed)
            for duty_cycle in range(100, -1, -step):
                p.ChangeDutyCycle(duty_cycle)
                time.sleep(speed)
            time.sleep(speed*20)
        except KeyboardInterrupt:
            return

def color_test_thread(target=color_test):
    threads = []
    frequency=300
    speed = 0.045
    step = 1

    threads = []
    for pin in PINOUT_MATRIX.flat:
        threads.append(threading.Thread(target=target, args=(pin, frequency, speed, step)))
    for t in threads:
        t.daemon = True
        t.start()
    for t in threads:
        t.join()
    
def simple_test(color_matrix=None):
    time_on = 0.001
    time_off = 0.001
    if color_matrix is None:
        color_matrix = all_intensity_matrix
    while True:
        update_lights(color_matrix)
        time.sleep(time_on)
        update_lights( zero_intensity_matrix)
        time.sleep(time_off)

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

def make_color_matrix(color):
    if not isinstance(color, int):
        color = COLOR_MAP[color]

    out_matrix = zero_intensity_matrix.copy()
    n_lights = out_matrix.shape[0]
    for i in range(n_lights):
        out_matrix[i, color] = GPIO.HIGH

    return out_matrix


if __name__ == '__main__':
    main()
