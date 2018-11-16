import RPi.GPIO as GPIO
import time
from collections import namedtuple
import numpy as np
import threading
from args_from_cmd import ArgsFromCMD
import math

red = [1, 0, 0]
green = [0, 1, 0]
blue = [0, 0, 1]
orange = [1, 1, 0]
purple = [1, 0, 1]
cyan = [0, 0, 1]
yellow = [1, 1, 1]
black = [0, 0, 0]
COLOR_MAP = {'r': red, 
             'g': green, 
             'b': blue, 
             'o': orange, 
             'p': purple,
             'c': cyan,
             'y': yellow,
             'k': black}
N_COLOR = 3


class ColorDesigner(ArgsFromCMD):
    #: base class for other ways to make lights
    def __init__(self, color_matrix):
        super(ColorDesigner, self).__init__(description="Color Designer")
        self.color_matrix = color_matrix
        self.n_lights = color_matrix.shape[0]
    
    def set_color_matrix(self):
        raise NotImplementedError

    def run(self):
        self.set_color_matrix()

class MakeMatrixColor(ColorDesigner):

    def __init__(self, color_matrix):
        super(MakeMatrixColor, self).__init__(color_matrix)

    def set_args(self):
        self.parser.add_argument("-c", "--color",
                type=str, choices=COLOR_MAP.keys(), default='r',
                help='the rgb opcy option')

    def process_args(self):
        if isinstance(self.args['color'], str):
            color = COLOR_MAP[self.args['color']]
        self.color = color
    
    def set_color_matrix(self):
        for light_ndx in range(self.n_lights):
            for color_ndx, color_val in enumerate(self.color):
                self.color_matrix[light_ndx, color_ndx] = GPIO.HIGH * color_val


class MakePWMColor(MakeMatrixColor):
 
    def __init__(self, color_matrix):
        super(MakePWMColor, self).__init__(color_matrix)
        self.start_time = time.time()

    def set_args(self):
        super(MakePWMColor, self).set_args()
        self.parser.add_argument("-f",'--frequency',
                type=float, default = 100.0,
                help='1 / arbitrary time units')
    
    def set_color_matrix(self):
        now_time = time.time()
        is_on = math.cos((now_time-self.start_time) * self.frequency / (2 * math.pi)) > 0
        
        for light_ndx in range(self.n_lights):
            for color_ndx, color_val in enumerate(self.color):
                self.color_matrix[light_ndx, color_ndx] = GPIO.HIGH * color_val * is_on
            
#: Add to light controller a 'run_until' node. This will allow it to run until a specified time and then pass information to the next light controller. 
