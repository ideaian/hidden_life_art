import RPi.GPIO as GPIO
import time
from collections import namedtuple
import numpy as np
import threading
import argparse
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


class ColorDesigner(object):
    #: base class for other ways to make lights
    def __init__(self, color_mat):
        self.color_mat = color_mat
        self.n_lights = color_mat.shape[0]
        self.parser = argparse.ArgumentParser(description="Make Single Color")
        self.set_args()
        self.get_args()
        self.process_args()
        self.cleanup_args()
    
    def set_args(self):
        pass

    def get_args(self):

        args, unused_args = self.parser.parse_known_args()
        if unused_args is not None:
            msg = 'Warning! Unused/unrecognized arguments: {}'.format(unused_args)
            print(msg)
        self.args = vars(args)

    def process_args(self):
        pass
    
    def cleanup_args(self):
        del self.parser

    def set_color_mat(self):
        raise NotImplementedError

    def run(self):
        self.set_color_mat()

#class MakeMatrixColor(object):
class MakeMatrixColor(ColorDesigner):

    def __init__(self, color_mat):
        super(MakeMatrixColor, self).__init__(color_mat)

    def set_args(self):
        self.parser.add_argument("-c", "--color",
                type=str, choices=COLOR_MAP.keys(), default='r',
                help='the rgb opcy option')

    def process_args(self):
        if isinstance(self.args['color'], str):
            color = COLOR_MAP[self.args['color']]
        self.color = color
    
    def set_color_mat(self):
        for light_ndx in range(self.n_lights):
            for color_ndx, color_val in enumerate(self.color):
                self.color_mat[light_ndx, color_ndx] = GPIO.HIGH * color_val


class MakePWMColor(MakeMatrixColor):
 
    def __init__(self, color_mat):
        super(MakePWMColor, self).__init__(color_mat)

    def set_args(self):
        self.p.add_argument("-f",'--frequency',
                type=float, default = 100.0,
                help='1 / arbitrary time units')
    
    def set_color_mat(self):
        pass
#: Add to light controller a 'run_until' node. This will allow it to run until a specified time and then pass information to the next light controller. 
