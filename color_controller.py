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
COLOR_MAP = {'r': red, 
             'g': green, 
             'b': blue, 
             'o': orange, 
             'p': purple,
             'c': cyan,
             'y': yellow}
N_COLOR = 3


class ColorDesigner(object):
    #: base class for other ways to make lights
    def __init__(self, color_mat):
        self.color_mat = color_mat
        self.n_lights = color_mat.shape[0]
        self.get_args()
        self.process_args()
    
    def get_arg(self):
        p = argparse.ArgumentParser(description="Highest Class")

    def process_args(self):
        pass

    def update_color_mat(self):
        pass

    def run(self):
        self.update_color_mat()

#class MakeMatrixColor(object):
class MakeMatrixColor(ColorDesigner):

    def __init__(self, color_mat):
        super(MakeMatrixColor, self).__init__(color_mat)

    def get_args(self):
        p = argparse.ArgumentParser(description="Make Single Color")
        p.add_argument("-c", "--color",
                type=str, choices=COLOR_MAP.keys(), default='r',
                help='the rgb opcy option')

        args, unused_args= p.parse_known_args()
        if unused_args is not None:
            msg = 'Warning! Unused/unrecognized arguments: {}'.format(unused_args)
            print(msg)
        self.args = vars(args)
    
    def process_args(self):
        if isinstance(self.args['color'], str):
            color = COLOR_MAP[self.args['color']]
        self.color = color

    def update_color_mat(self):
        for light_ndx in range(self.n_lights):
            for color_ndx, color_val in enumerate(self.color):
                self.color_mat[light_ndx, color_ndx] = GPIO.HIGH * color_val


class MakePWMColor(MakeMatrixColor):
 
    def __init__(self, color_mat):
        super(MakePWMColor, self).__init__(color_mat)

    def get_args(self):
        p = argparse.ArgumentParser(description="PWM color")
        p.add_argument("-f",'--frequency',
                type=float

#: Add to light controller a 'run_until' node. This will allow it to run until a specified time and then pass information to the next light controller. 
