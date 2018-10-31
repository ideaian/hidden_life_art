import RPi.GPIO as GPIO
import time
from collections import namedtuple
import numpy as np
import threading

#:wGPIO.setwarnings(False)
PINOUT_MATRIX = \
        np.array([[12, 21, 23],
                  [24, 25, 16],
                  [13, 26, 14],
                  [17, 22, 5]
                  ], dtype=int)
zero_intensity_matrix = GPIO.LOW * np.ones(shape=PINOUT_MATRIX.shape, dtype=int)
all_intensity_matrix = GPIO.HIGH * np.ones(shape=PINOUT_MATRIX.shape, dtype=int)

COLOR_MAP = {'r':0, 'g':1, 'b':2}

def main():
    GPIO.setmode(GPIO.BCM)



    init_gpio_pins()

    try:
        #color_test_thread()
        simple_test()
    except (KeyboardInterrupt, SystemExit):
        print("Exiting")
    finally:
        print("Cleaning up")
        update_lights(zero_intensity_matrix)    
        update_lights(zero_intensity_matrix)    
        GPIO.cleanup()

def color_test(pin, frequency, speed, step):
    p = GPIO.PWM(pin, frequency)
    p.start(0)
    while True:
        for duty_cycle in range(0, 101, step):
            p.ChangeDutyCycle(duty_cycle)
            time.sleep(speed)
        for duty_cycle in range(100, -1, -step):
            p.ChangeDutyCycle(duty_cycle)
            time.sleep(speed)

def color_test_thread():
    threads = []
    frequency=300
    speed = 0.045
    step = 1

    threads = []
    for pin in PINOUT_MATRIX.flat:
        threads.append(threading.Thread(target=color_test, args=(pin, frequency, speed, step)))
    for t in threads:
        t.daemon = True
        t.start()
    for t in threads:
        t.join()
    

def simple_test():
    time_on = 0.001
    time_off = 0.001
    while True:
        update_lights(all_intensity_matrix)
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

def make_color_matrix(n_lights, color):

    out_matrix = np.ones(shape=(n_lights, 3), dtype=int) * GPIO.LOW
    for i in range(n_lights):
        out_matrix[i, color] = GPIO.HIGH

    return out_matrix


if __name__ == '__main__':
    main()
