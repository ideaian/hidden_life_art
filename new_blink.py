import RPi.GPIO as GPIO
import time
from collections import namedtuple
import numpy as np
import threading


from light_controller import (
        COLOR_MAP, ColorFromGlobalWriter, MakeMatrixColor
)

#can make importing color makers and names automatic maybe and providing the list of available color_dsigners
from simple_class import SimpleClass
#: This should be specified by a yaml
AVAILABLE_COLOR_DESIGNERS = {'simple_class': SimpleClass,  'one_color': MakeMatrixColor}
PINOUT_MATRIX = \
        np.array([[25, 24, 23],
                  [16, 21, 20],
                  [13, 19, 26],
                  [17, 22, 27]
                  ], dtype=int)


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


def get_args():
    import sys
    import argparse

    p = argparse.ArgumentParser(description="Make colors")

    p.add_argument("--color_designer", required=True,
            type=str, choices=AVAILABLE_COLOR_DESIGNERS.keys(), default=None,
            help="One of the available color designer functions in the list {}".format(AVAILABLE_COLOR_DESIGNERS.keys()))
    args, _ = p.parse_known_args() 

    return vars(args)


def get_color_designer(args):
    cd = AVAILABLE_COLOR_DESIGNERS[args['color_designer']]
    
    return cd


def main():
    
    args = get_args()
    color_designer = get_color_designer(args)
    gcw = ColorFromGlobalWriter(
            pinout = PINOUT_MATRIX,
            gpio_mode = 'bcm',
            color_designer = color_designer,
            )
    gcw.initialize_threads() 
    try:
        gcw.start_threads() 
    except (KeyboardInterrupt, SystemExit):
        print("Exiting")
    finally:
        print("Cleaning up")
        gcw.exit()


if __name__ == '__main__':
    main()
