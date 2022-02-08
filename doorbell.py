#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import os

relay_pin=23
door_pin=24

GPIO.setmode(GPIO.BCM)
GPIO.setup(door_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(relay_pin, GPIO.OUT)

GPIO.output(relay_pin, True)

class Chime(object):
    def __init__(self):
        self.status = False

    def set(self, status):
        self.status = status

    def get(self):
        return self.status

def sensor(chime): 
    if GPIO.input(door_pin) == GPIO.HIGH:
        if chime: 
            GPIO.output(relay_pin, False)
        return True
    else: 
        if chime: 
            GPIO.output(relay_pin, True)
        return False

def test():
    GPIO.output(relay_pin, False)
    time.sleep(0.5)
    GPIO.output(relay_pin, True)
    
