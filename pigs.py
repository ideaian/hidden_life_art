
RED_PIN=17
GREEN_PIN=22
BLUE_PIN=24
PIN=BLUE_PIN
BRIGHTNESS=0.5
import pigpio
pi = pigpio.pi()
pi.set_PWM_dutycycle(PIN, BRIGHTNESS)
pi.stop()
