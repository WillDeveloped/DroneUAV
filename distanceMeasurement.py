import pygame 
import cv2
import numpy as np
import threading
import time
import pandas
from djitellopy import Tello


height = []
pitch = []
roll = []
yaw = []
speed_x = []
speed_y = []
speed_z = []
acc_x = []
acc_y = []
acc_z = []
now = []


drone = Tello()
drone.connect()

def getTelemetry():
    while True:
        '''
        This is going to run in a loop for the entire duration of the flight. Need to research into "get_current_state()" to see if it will just return all these values instead of doing all these calls a bunch of times, just do the one call, update the information, and repeat 
        '''
        height = drone.get_height()
        pitch = drone.get_pitch()
        roll = drone.get_roll()
        yaw = drone.get_yaw()
        speed_x = drone.get_speed_x()
        speed_y = drone.get_speed_y()
        speed_z = drone.get_speed_z()
        acc_x = drone.get_acceleration_x()
        acc_y = drone.get_acceleration_y()
        acc_z = drone.get_acceleration_z()
        now = time.time()


def moveForward():
    drone.takeoff()
    drone.get_current_state()
    time.sleep(2) #Should be enough time to get off the ground
    drone.move(10)
    drone.land()
