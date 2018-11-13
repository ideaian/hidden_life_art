import RPi.GPIO as GPIO
import time
from collections import namedtuple
import numpy as np
import threading


from light_controller import (
        ColorFromGlobalWriter
)
from color_controller import (
         MakePWMColor, MakeMatrixColor, COLOR_MAP
)

#: This should be specified by a yaml
AVAILABLE_COLOR_DESIGNERS = {'one_color': MakeMatrixColor,
                             'pwm_color': MakePWMColor
                             }
PINOUT_MATRIX = \
        np.array([[25, 24, 23],
                  [16, 21, 20],
                  [13, 19, 26],
                  [17, 22, 27]
                  ], dtype=int)

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
