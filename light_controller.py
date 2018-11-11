import RPi.GPIO as GPIO
import time
from collections import namedtuple
import numpy as np
import threading
from killable_threads import ThreadWithExc

red = [1, 0, 0]
green = [0, 1, 0]
blue = [0, 0, 1]
COLOR_MAP = {'r': red, 'g': green, 'b': blue}
N_COLOR = 3
GPIO_MODES = {'bcm': GPIO.BCM, 'board': GPIO.BOARD}

class LightController(object):
    def __init__(self, pinout, gpio_mode='bcm'):
        if gpio_mode not in GPIO_MODES.keys():
            msg = 'Mode {} not available in list of {}'.format(gpio_modes.keys())
            raise ValueError(msg)
        gpio_mode = GPIO_MODES[gpio_mode]
        GPIO.setmode(gpio_mode)
        self.pinout= pinout
        self.color_matrix = pinout * 0
        self.zero_mat = GPIO.LOW * np.ones(shape=pinout.shape, dtype=int)
        self.one_mat = GPIO.HIGH * np.ones(shape=pinout.shape, dtype=int)
        self.init_pinout()
        self.write_threads=True
        #self.cleaned

    def init_pinout(self):
        for pin in iter(self.pinout.flat):
            GPIO.setup(pin, GPIO.OUT)
    
    def gpio_writer(self):
        i=0
        while self.write_threads:
            try:
                if i%1000==0:
                    print(i)
                i+=1
                self.color_designer(self.color_matrix, self.color_designer_args)
                for pin, intensity in zip(self.pinout.flat, self.color_matrix.flat):
                    GPIO.output(pin, intensity)
                
            except KeyboardInterrupt:
                print("Interrupt in gpio writer")
                return
        print("write threads is {}".format(self.write_threads))
                
    
    def exit(self, exc_type=None, exc_value=None, traceback=None):
	print("Cleaning up on ex_type")
        self.write_threads = False
	self.color_matrix = self.zero_mat
        self.gpio_writer()
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
        self.exception_checker_thread = None

    def initialize_threads(self):
        self.threads = []
        NO_ARGS = ()
        writer_thread = threading.Thread(name='writer', 
               target=self.gpio_writer, args=NO_ARGS)
        writer_thread.daemon=True
        self.threads.append(writer_thread)

    def start_threads(self):
        #self.exception_checker_thread.start()
        for t in self.threads:
            print("thread {} started".format(t.name))
            t.start()
        while True:
            try:
                pass
            except KeyboardInterrupt:
                print('interrupt in threads')
                self.write_threads = False
                return

    def color_designer(self):
        raise NotImplementedError

        
    

