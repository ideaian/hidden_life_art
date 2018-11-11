import RPi.GPIO as GPIO
import time
from collections import namedtuple
import numpy as np
import threading

COLOR_MAP = {'r': [1, 0, 0], 'g':[0, 1, 0], 'b': [0, 0, 1]}

class LightController(object):
    def __init__(self, pinout, gpio_mode):
        gpio_modes = {'bcm': GPIO.BCM, 'board': GPIO.BOARD}
        if gpio_mode not in gpio_modes.keys():
            msg = 'Mode {} not available in list of {}'.format(gpio_modes.keys())
            raise ValueError(msg)
  
        GPIO.setmode(GPIO.BCM)
        GPIO.setmode(gpio_mode)
        self.pin_mat= pinout
        self.color_matrix = pinout * 0
        #:GPIO.setwarnings(False)
        self.zero_mat = GPIO.LOW * np.ones(shape=PINOUT_MATRIX.shape, dtype=int)
        self.one_mat = GPIO.HIGH * np.ones(shape=PINOUT_MATRIX.shape, dtype=int)
        self.init_gpio_pins()

    def init_gpio_pins():
        for pin in iter(self.pinout.flat):
            GPIO.setup(pin, GPIO.OUT)

    def update_state(intensity_matrix, changed_state=True):
        if not changed_state:
            return
        for (pin, intensity) in zip(PINOUT_MATRIX, intensity_matrix):
            update_string(pin, intensity)
    
    def gpio_writer(self):
        for pin, intensity in zip(self.pinout.flat, self.color_matrix.flat):
            GPIO.output(pin, intensity)
    
    def __exit__(self, exc_type, exc_value, traceback):
	print("Cleaning up on ex_type{}").format(ex_type)
 	self.update_lights(zero_intensity_matrix)
	GPIO.cleanup() 


class ColorFromGlobalWriter(LightController):
   
    def __init__(self, gpio_pins, gpio_mode, 
                 color_designer=None, color_designer_args=None,
                 color_writer):
        super(LightController, self).__init__(gpio_pins, gpio_mode)
        self.color_designer = color_designer
        self.color_designer_args = color_designer_args
        if color_designer is None or thread_writer is None:
            msg = 'Nothing to do as no designer was {} and writer was {}'
            raise ValueError(msg)

    def initialize_threads(self):
        threads = []
        #: this is where I would append a listener thread.
        designer_thread = threading.Thread(target=self.color_designer, 
                                     args=(self.color_mat, self.color_designer_args))
        threads.append(designer_thread)
        writer_thread = threading.Thread(target=self.gpio_writer, args=None)
        threads.append(writer_thread)

    def start_threads(self):
        for t in self.threads:
            t.daemon = True
            t.start()
        for t in self.threads:
            t.join()

    def color_designer(self):
        raise NotImplementedError

        
def make_single_matrix(color_mat, color):
    n_lights = out_matrix.shape[0]
    if isinstance(color, str):
        color = COLOR_MAP[color]
    for light_ndx in range(n_lights):
        for color, colr_ndx in enumrate(color):
            color_mat[light_ndx, colr_ndx] = GPIO.HIGH * color


            def ColorDesigner(object):


