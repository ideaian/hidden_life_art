import RPi.GPIO as GPIO
import time
from collections import namedtuple
import numpy as np
import threading


from light_controller import (
        LightController, PWMLightController
)
from color_controller import (
         MakePWMColor, MakeMatrixColor, COLOR_MAP
)

#: This should be specified by a yaml
AVAILABLE_COLOR_DESIGNERS = {'one_color': MakeMatrixColor,
                             'pwm_color': MakePWMColor
                             }

AVAILABLE_LIGHT_CONTROLLERS = {'solid': LightController,
                     'pwm': PWMLightController}
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
    p.add_argument("--light_controller",
            type=str, choices=AVAILABLE_LIGHT_CONTROLLERS.keys(), default='solid',
            help="One of the available color designer functions in the list {}".format(AVAILABLE_LIGHT_CONTROLLERS.keys()))
    p.add_argument("--color_designer",
            type=str, choices=AVAILABLE_COLOR_DESIGNERS.keys(), default='one_color',
            help="One of the available color designer functions in the list {}".format(AVAILABLE_COLOR_DESIGNERS.keys()))
    args, _ = p.parse_known_args() 

    return vars(args)


def get_color_designer(args):
    cd = AVAILABLE_COLOR_DESIGNERS[args['color_designer']]
    return cd

def get_light_controller(args):
    lc = AVAILABLE_LIGHT_CONTROLLERS[args['light_controller']]
    return lc

def main():
    
    args = get_args()
    color_designer = get_color_designer(args)
    light_controller = get_light_controller(args)
    gcw = light_controller(
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
