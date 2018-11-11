import RPi.GPIO as GPIO
import time
from collections import namedtuple
import numpy as np
import threading

COLOR_MAP = {'r': [1, 0, 0], 'g':[0, 1, 0], 'b': [0, 0, 1]}
red = [1, 0, 0]
green = [0, 1, 0]
blue = [0, 0, 1]
N_COLOR = 3
GPIO_MODES = {'bcm': GPIO.BCM, 'board': GPIO.BOARD}

class LightController(object):
    def __init__(self, pinout, gpio_mode):
        if gpio_mode not in GPIO_MODES.keys():
            msg = 'Mode {} not available in list of {}'.format(gpio_modes.keys())
            raise ValueError(msg)
        gpio_mode = GPIO_MODES[gpio_mode]
        GPIO.setmode(GPIO.BCM)
        GPIO.setmode(gpio_mode)
        self.pinout= pinout
        self.color_matrix = pinout * 0
        #:GPIO.setwarnings(False)
        self.zero_mat = GPIO.LOW * np.ones(shape=pinout.shape, dtype=int)
        self.one_mat = GPIO.HIGH * np.ones(shape=pinout.shape, dtype=int)
        self.init_pinout()

    def init_pinout(self):
        for pin in iter(self.pinout.flat):
            GPIO.setup(pin, GPIO.OUT)
    
    def gpio_writer(self):
        for pin, intensity in zip(self.pinout.flat, self.color_matrix.flat):
            GPIO.output(pin, intensity)
    
    def __exit__(self, exc_type, exc_value, traceback):
	print("Cleaning up on ex_type{}").format(ex_type)
 	self.make_single_matrix([0, 0, 0])
	GPIO.cleanup() 


class ColorFromGlobalWriter(LightController):
   
    def __init__(self, pinout, gpio_mode, 
                 color_designer=None, color_designer_args=None):
        super(ColorFromGlobalWriter, self).__init__(pinout, gpio_mode)
        self.color_designer = color_designer
        self.color_designer_args = color_designer_args
        if color_designer is None:
            msg = 'Nothing to do as no designer was {} and writer was {}'
            raise ValueError(msg)
        self.threads = []

    def initialize_threads(self):
        self.threads = []
        #: this is where I would append a listener thread.
        designer_thread = threading.Thread(target=self.color_designer, 
                                     args=(self.color_matrix, self.color_designer_args))
        self.threads.append(designer_thread)
        NO_ARGS = ()
        writer_thread = threading.Thread(target=self.gpio_writer, args=NO_ARGS)
        self.threads.append(writer_thread)

    def start_threads(self):
        for t in self.threads:
            t.daemon = True
            t.start()
        for t in self.threads:
            t.join()

    def color_designer(self):
        raise NotImplementedError

        
def make_single_matrix(color_mat, color):
    'color is a 1x3 matrix'
    n_lights = color_mat.shape[0]
    for light_ndx in range(N_COLOR):
        for color, colr_ndx in enumrate(color):
            color_mat[light_ndx, colr_ndx] = GPIO.HIGH * color

def update_state(intensity_matrix, changed_state=True):
    if not changed_state:
        return
    for (pin, intensity) in zip(PINOUT_MATRIX, intensity_matrix):
        update_string(pin, intensity)
#def ColorDesigner(object):
    

