import RPi.GPIO as GPIO
import time
from collections import namedtuple
import numpy as np
import threading


from light_controller import (
        COLOR_MAP, ColorFromGlobalWriter
)

#: This should be specified by a yaml
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

# make_color matrix and get_args can be bundled into a general class
def make_color_matrix(color_mat, color):
    n_lights = color_mat.shape[0]
    color = color['color_designer_args']
    if isinstance(color, str):
        color = COLOR_MAP[color]
    while True:
        try:
            for light_ndx in range(n_lights):
                for color_val, colr_ndx in enumerate(color):
                    color_mat[light_ndx, colr_ndx] = GPIO.HIGH * color_val
        except KeyboardInterrupt:
            return


def get_args():
    import sys
    import argparse

    p = argparse.ArgumentParser(description="Make colors")
    
    p.add_argument("-c", "--color_designer_args", 
            type=str, choices=['r','g','b'], default='r',
                   help="increase output verbosity")
    return vars(p.parse_args()) 


def main():
    
    args = get_args()
    color_designer_args = args
    gcw = ColorFromGlobalWriter(
            pinout = PINOUT_MATRIX,
            gpio_mode = 'bcm',
            color_designer = make_color_matrix,
            color_designer_args=color_designer_args
            )
    gcw.initialize_threads() 
    try:
        gcw.start_threads() 
    except (KeyboardInterrupt, SystemExit):
        print("Exiting")
    finally:
        print("Cleaning up")
        GPIO.cleanup()



if __name__ == '__main__':
    main()
