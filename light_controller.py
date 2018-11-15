import RPi.GPIO as GPIO
import time
from collections import namedtuple
import numpy as np
import threading
from args_from_cmd import ArgsFromCMD

GPIO_MODES = {'bcm': GPIO.BCM, 'board': GPIO.BOARD}


class LightController(ArgsFromCMD):
    def __init__(self, pinout, gpio_mode='bcm', color_designer=None):
        super(LightController, self).__init__(description='Light Controller')
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

        if color_designer is None:
            msg = 'Nothing to do as no designer was none'
            raise ValueError(msg)
        self.color_designer = color_designer(color_matrix=self.color_matrix)
        self.threads = []
        self.exception_checker_thread = None

    def init_pinout(self):
        for pin in iter(self.pinout.flat):
            GPIO.setup(pin, GPIO.OUT)
    
    def design_and_write(self):
        pass

    def gpio_write_zero(self):
        for pin, intensity in zip(self.pinout.flat, self.color_matrix.flat):
            GPIO.output(pin, GPIO.LOW)
    
    def gpio_writer(self):
        for pin, intensity in zip(self.pinout.flat, self.color_matrix.flat):
            GPIO.output(pin, intensity)

    def exit(self):
        print("Cleaning threads")
        self.write_threads = False
        print("Cleaning pins")
        time.sleep(0.1)
        self.color_matrix = self.zero_mat
        self.gpio_writer()
        time.sleep(0.1)
        GPIO.cleanup() 

    def initialize_threads(self):
        self.threads = []
        NO_ARGS = ()
        writer_thread = threading.Thread(name='designer and writer', 
               target=self.design_and_write, args=NO_ARGS)
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

    def design_and_write(self):
        while self.write_threads:
            try:
                print('run')
                self.color_designer()
                print('write')
                self.gpio_writer()
            except KeyboardInterrupt:
                print("Interrupt in gpio writer")
                self.exit()
                return
    
    def color_designer(self):
        raise NotImplementedError


class PWMLightController(LightController):
    def __init__(self, pinout, gpio_mode='bcm', color_designer=None):
        super(PWMLightController, self).__init__()
    
    def set_args(self):
        self.parser.add_argument("-f", "--frequency", type=float, default=100.0,
                help="1 / arb time units")
        self.parser.add_argument("-d", "--frac_time_on", type=float, default=0.5,
                help="Fraction of time colors are on (duty cycle).")
        
    
    def process_args(self):
        if (self.args['frac_time_on'] > 1.0) or (self.args['frac_time_on'] < 0):
            msg = "Specified duty cycle {} invalid on range [0, 1]".format(self.args['frac_time_on'])
            raise ValueError(msg)
        self.time_on = self.args['frac_time_on']/ self.args['frequency']
        self.time_on = (1.0 - self.args['frac_time_on'])/ self.args['frequency']
        
    def pwm_design_and_write(self):
        while self.write_threads:
            try:
                self.gpio_writer()
                time.sleep(self.time_on)
                self.gpio_write_zero()
                time.sleep(self.time_off)

            except KeyboardInterrupt:
                print("Interrupt in gpio writer")
                self.exit()
                return
