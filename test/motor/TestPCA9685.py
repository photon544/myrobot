# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time

import argparse

# Import the PCA9685 module.
import Adafruit_PCA9685

# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)



# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)




def servo_test():
    # Configure min and max servo pulse lengths
    servo_min = 150  # Min pulse length out of 4096
    servo_max = 600  # Max pulse length out of 4096
    # Set frequency to 60hz, good for servos.
    pwm.set_pwm_freq(60)
    
    print('Moving servo on channel 0, press Ctrl-C to quit...')
    while True:
        # Move servo on channel O between extremes.
        pwm.set_pwm(1, 0, servo_min)
        time.sleep(2)
        pwm.set_pwm(1, 0, servo_max)
        time.sleep(2)
        
def H_Bridge_test():
    # Configure min and max servo pulse lengths
    servo_min = 1000  # Min pulse length out of 4096
    servo_max = 2000  # Max pulse length out of 4096
    # Set frequency to 60hz, good for servos.
    pwm.set_pwm_freq(60)
    
    print('Moving servo on channel 0, press Ctrl-C to quit...')
    # while True:
    # Move servo on channel O between extremes.
    pwm.set_pwm(4, 0, servo_min)
    time.sleep(2)
    pwm.set_pwm(4, 0, servo_max)
    time.sleep(2)
    pwm.set_pwm(4, 0, 0)
    time.sleep(2)
    pwm.set_pwm(5, 0, servo_max)
    time.sleep(2)
    pwm.set_pwm(5, 0, 0)

def motor_driver(motor_id, speed):  # speed in [-1, 1]
    # 0   8  9
    # 1   10 11
    # 2   12 13
    # 3   14 15
    pin_id = 8 + 2 * motor_id
    
    pwm.set_pwm(pin_id, 0, 0)
    pwm.set_pwm(pin_id + 1, 0, 0)
    if speed < 0:
        pin_id = pin_id + 1
        speed *= -1.0
    pulse = int(1000 + (4096-1000) * speed)
    if pulse >= 4096:
        pulse = 4095
    if speed < 0.001:
        pulse = 0
    pwm.set_pwm(pin_id, 0, pulse)
    
def motor_test(channel, speed):
    pwm.set_pwm_freq(50)
    motor_driver(channel, speed)
    time.sleep(2)
    motor_driver(channel, speed*(-1.0))
    time.sleep(2)
    motor_driver(channel, 0)

def forward(speed):
    pwm.set_pwm_freq(50)
    for channel in range(4):
        speed_inner = speed
        if channel == 1:
            speed_inner = - speed
        motor_driver(channel, speed_inner)

def left(speed):
    pwm.set_pwm_freq(50)
    for channel in range(4):
        speed_inner = speed
        if channel == 1:
            speed_inner = - speed
        if channel %2 == 1:
            # speed_inner = 0.2* speed_inner
            speed_inner = 0
        motor_driver(channel, speed_inner)

def right(speed):
    pwm.set_pwm_freq(50)
    for channel in range(4):
        speed_inner = speed
        if channel == 1:
            speed_inner = - speed
        if channel %2 == 0:
            #speed_inner = 0.2* speed_inner
            speed_inner = 0
        motor_driver(channel, speed_inner)

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--function", help="choose the function to test: motor, servo, car", choices=['motor', 'servo', 'car'],
                    default='motor')
parser.add_argument("-d", "--direction", help="choose the direction", choices=['forward', 'backword', 'left', 'right'],
                    default='forward')
parser.add_argument("-c", "--channel", type=int, help="choose the motor channel", choices=range(4),
                    default=0)
parser.add_argument("-s", "--speed", type = float, help="the speed of the motor",
                    default=0.5)
args = parser.parse_args()


if __name__ == '__main__':
    if args.function == 'motor':
    #H_Bridge_test()
        motor_test(args.channel, args.speed)
    if args.function == 'servo':
        servo_test()
    if args.function == 'car':
        if args.direction == 'forward':
            forward(args.speed)
            time.sleep(2)
            forward(0)
        if args.direction == 'left':
            left(args.speed)
            time.sleep(1)
            forward(0)
        if args.direction == 'right':
            right(args.speed)
            time.sleep(1)
            forward(0)

