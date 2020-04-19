#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

def motor_test():
    ################################# DC motor test!
    myMotor = mh.getMotor(3)
    
    # set the speed to start, from 0 (off) to 255 (max speed)
    myMotor.setSpeed(150)
    myMotor.run(Adafruit_MotorHAT.FORWARD);
    # turn on motor
    myMotor.run(Adafruit_MotorHAT.RELEASE);
    
    
    
    while (True):
        print("Forward! ")
        myMotor.run(Adafruit_MotorHAT.FORWARD)
    
        print("\tSpeed up...")
        for i in range(255):
            myMotor.setSpeed(i)
            time.sleep(0.01)
    
        print("\tSlow down...")
        for i in reversed(range(255)):
            myMotor.setSpeed(i)
            time.sleep(0.01)
    
        print("Backward! ")
        myMotor.run(Adafruit_MotorHAT.BACKWARD)
    
        print("\tSpeed up...")
        for i in range(255):
            myMotor.setSpeed(i)
            time.sleep(0.01)
    
        print("\tSlow down...")
        for i in reversed(range(255)):
            myMotor.setSpeed(i)
            time.sleep(0.01)
    
        print("Release")
        myMotor.run(Adafruit_MotorHAT.RELEASE)
        time.sleep(1.0)

def my_dc_test():
    motors = [mh.getMotor(1), mh.getMotor(2), mh.getMotor(3), mh.getMotor(4)]
    my_motor = motors[0]
    # set the speed to start, from 0 (off) to 255 (max speed)
    my_motor.setSpeed(150)
    my_motor.run(Adafruit_MotorHAT.FORWARD);
    # turn on motor
    #time.sleep(1)
    my_motor.run(Adafruit_MotorHAT.RELEASE);
    
    #print("Forward! ")
    #my_motor.run(Adafruit_MotorHAT.FORWARD)
    for motor in motors:
        print("Forward! ")
        motor.setSpeed(100)
        motor.run(Adafruit_MotorHAT.FORWARD);
        time.sleep(1)
        motor.run(Adafruit_MotorHAT.RELEASE);
        time.sleep(0.5)
        
    for motor in motors:
        print("Backward! ")
        motor.setSpeed(100)
        motor.run(Adafruit_MotorHAT.BACKWARD);
        time.sleep(1)
        motor.run(Adafruit_MotorHAT.RELEASE);
        time.sleep(0.5)
        
    #print("\tSpeed up...")
    #for i in range(255):
    #    my_motor.setSpeed(i)
    #    time.sleep(0.01)
            
            
if __name__ == "__main__":
    #motor_test()
    my_dc_test()
    
    # main()
    # test()