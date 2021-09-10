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
            'mid': -1, 
            'x': -100, 
            'y': -100, 
            'z': -100, 
            'mpry': '0,0,0', 
            'pitch': 0, 
            'roll': -1, 
            'yaw': 5, 
            'vgx': 0, 
            'vgy': 0, 
            'vgz': 0, 
            'templ': 56, 
            'temph': 59, 
            'tof': 10, 
            'h': 0, 
            'bat': 6, 
            'baro': 412.3, 
            'time': 0, 
            'agx': 0.0, 
            'agy': 20.0, 
            'agz': -998.0
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
       
    
