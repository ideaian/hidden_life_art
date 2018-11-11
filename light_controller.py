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
        #:GPIO.setwarnings(False)
        self.zero_mat = GPIO.LOW * np.ones(shape=pinout.shape, dtype=int)
        self.one_mat = GPIO.HIGH * np.ones(shape=pinout.shape, dtype=int)
        self.init_pinout()
        self.KBI = [False]

    def init_pinout(self):
        for pin in iter(self.pinout.flat):
            GPIO.setup(pin, GPIO.OUT)
    
    def gpio_writer(self):
        while True:
            i=0
            try:
                i+=1
                if i%1000==0:
                    print("writer")
                for pin, intensity in zip(self.pinout.flat, self.color_matrix.flat):
                    GPIO.output(pin, intensity)
                
                if self.KBI[0]:
                    print("external interrupt")
                    break
            except KeyboardInterrupt:
                print("Interrupt in gpio writer")
                return
                
    
    def __exit__(self, exc_type=None, exc_value=None, traceback=None):
	print("Cleaning up on ex_type")
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
        self.exception_checker_thread = ThreadWithExc(target=None, args=NO_ARGS)
        #self.exception_checker_thread.daemon = True
        
        #: this is where I would append a listener thread.
        designer_thread = ThreadWithExc(name='designer',target=self.color_designer, 
                                     args=(self.color_matrix, self.KBI, self.color_designer_args))
        #designer_thread.daemon = True
        self.threads.append(designer_thread)
        writer_thread = ThreadWithExc(name='writer', 
               target=self.gpio_writer, args=NO_ARGS)
        #writer_thread.daemon=True
        self.threads.append(writer_thread)

    def start_threads(self):
        self.exception_checker_thread.start()
        for t in self.threads:
            print("thread {} started".format(t.name))
            t.start()
        print("all threads started")
        #for t in self.threads:
        #    print("thread {} joined".format(t.name))
        #    t.join()
        #print('here')
        #while self.exception_checker_thread.isAlive():
        #    time.sleep( 0.1 )
        #    print('yo')
        #print('end')
        #self.__exit__(exc_type=KeyboardInterrupt)


    def color_designer(self):
        raise NotImplementedError

        
    

