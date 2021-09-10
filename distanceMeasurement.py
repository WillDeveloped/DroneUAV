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
print(drone.get_current_state())

def getTelemetry():
    while True:
        '''
        This is going to run in a loop for the entire duration of the flight. Need to research into "get_current_state()" to see if it will just return all these values instead of doing all these calls a bunch of times, just do the one call, update the information, and repeat 
        
        response is: 
        {
            'mid': -1,          this is mission pad related
            'x': -100,          this is mission pad related
            'y': -100,          this is mission pad related
            'z': -100,          this is mission pad related
            'mpry': '0,0,0',    this is x, y and z all in one
            'pitch': 0,         pitch in degrees
            'roll': -1,         roll in degrees
            'yaw': 5,           yaw in degrees
            'vgx': 0,           speed_x
            'vgy': 0,           speed_y
            'vgz': 0,           speed_z
            'templ': 56,        temp_low °C 
            'temph': 59,        temp_high °C
            'tof': 10,          tof distance
            'h': 0,             height in cm
            'bat': 6,           battery percent
            'baro': 412.3,      barometer value in cm -abs height
            'time': 0,          flight time in s
            'agx': 0.0,         acceleration_x
            'agy': 20.0,        acceleration_y
            'agz': -998.0       acceleration_z
        }
        
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
    #drone.takeoff()
    drone = Tello()
    drone.connect()
    print(drone.get_current_state())
       
    
