import RPi.GPIO as GPIO
import time
from collections import namedtuple
import numpy as np
import threading

COLOR_MAP = {'r':0, 'g':1, 'b':2}

class LightController(object):
    def __init__(self, pin_matrix, gpio_mode):
        gpio_modes = {'bcm': GPIO.BCM, 'board': GPIO.BOARD}
        if gpio_mode not in gpio_modes.keys():
            msg = 'Mode {} not available in list of {}'.format(gpio_modes.keys())
            raise ValueError(msg)
  
        GPIO.setmode(GPIO.BCM)
        GPIO.setmode(gpio_mode)
        self.pin_mat= pin_matrix
        #:GPIO.setwarnings(False)
        self.zero_mat = GPIO.LOW * np.ones(shape=PINOUT_MATRIX.shape, dtype=int)
        self.one_mat = GPIO.HIGH * np.ones(shape=PINOUT_MATRIX.shape, dtype=int)


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

   def __exit__(self, exc_type, exc_value, traceback):
	print("Cleaning up on ex_type{}").format(ex_type)
 	self.update_lights(zero_intensity_matrix)
	GPIO.cleanup() 


'''
pulse_on
pulse_off

will eventually have sound->color modulation

color_designer will be a function that can take in sound/images other input and change the lights based on it

make a very simple function that will respond to key strokes to change the color based on key

a simple function that will pulse along the different strands

TODO:a function that tries to map the music into color in a generative fashion. NN-style:w

music -> mapping -> color estimate -> compare -> loss -> update

a function that analyzes the beat and gets in sync with it to execute its commands. 
c
'''

class ColorFromGlobalWriter(LightController):
    def __init__(self, gpio_pins, gpio_mode, color_designer=None, 
                 thread_writer=None, 
                 color_designer_args=None, color_writer_args=None):
        super(LightController, self).__init__(gpio_pins, gpio_mode)
        self.color_designer=color_designer
        self.thread_writer=thread_writer
        self.color_writer_args = color_writer_args
        self.color_designer_args = color_designer_args

    def start(self):
        if target is None:
            return
        threads = []
        threads.append(threading.Thread(target=self.color_designer, args=self.color_designer_args))
        for pin in PINOUT_MATRIX.flat:
	    thread = threading.Thread(target=self.target, args=self.args)
	    thread.daemon = True
            threads.append()
        for t in threads:
            t.daemon = True
            t.start()
        for t in threads:
            t.join()

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

'''
TODO: a simple funciton that can take in simple functions and execute them in order a function pipeline
def pipeline_func(data, fns):

    return reduce(lambda a, x: x(a),

                  fns,

                  data)
pipeline_func(nums, [even_filter,

                     multiply_by_three,

                     convert_to_string])

'''
