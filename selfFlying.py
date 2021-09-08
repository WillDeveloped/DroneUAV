import pygame 
import cv2
import numpy as np
import threading
import time

import keyboard as kb
from djitellopy import Tello


#This may not be needed anymore. Might be switching to 
#Move commands that wait for a response
velocity = [0, 0 ,0 ,0]
#programed as lr, fb, y, t 
#lr is left right
#fb is front back
#y is yaw
#t is throttle

drone = Tello()
drone.connect()
drone.set_video_fps(drone.Tello.FPS_30) 
drone.set_video_resolution(drone.Tello.RESOLUTION_720P)
drone.set_video_bitrate(drone.Tello.BITRATE_5MBPS)
drone.streamon()
 
def getDistanceFromDrone(intensity):
    '''
    Takes in an int representing the pixel intensity maximum
    in the field of concern from the drones flight path. Returns the distance to the object.
    Equation: f(x) = -.102x + 82.26
    '''
    return (-.102 * intensity) + 82.66


def takePhoto():
    '''
    Instructs the drone to take a picture, and get the positional data of the drone. Image should be passed through model, creating a monodepth image. Image should be stored as both the mono, and the original.

    Should this check to see if the drone is moving before taking a photo? For instance, if I call speed and acceleration, find a non-zero and a negative number, I can infer that the drone is slowing down. Should I wait until the speed and acceperation are both close to zero, before taking a photo? 
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

    pass

def collide():
    '''
    Returns true or false on whether a collision will happen. This method will take the output of the mono model, and determine if a collsion will happen based on the intensity of the pixels, along the current heading (represented by a certain amount of pixes x/y l/r (Need to determin this))


    Figureout what part of the drones photo is it's collision path. Meaning, draw a box in the image that the drone cares about. 

    
    Figureout how much the drone actually moves foward, when the minimum value is called.

    Figureout a scale on the drones photo, determining pixle intensity value and how it releates to distance away from the drone. Find minimum distance away from an object the image must be, and the furthest distance away from an object the drone can be to pick it up on the camera. 
    '''
    return False

def findBetterCourse():
    '''
    Takes the output produced by the model, and tries to find an heading in 3 dimensional space, and returns the needed corrections to take, prior to advancing. This method might
    make the moves it's self, then restart the process starting at take photo. 
    '''
    pass

def move():
    '''
    Might overload this method. Not sure.
    This method moves the drone in any direction needed
    '''
    pass

def main():
    '''
    The main loop of the program. The main loop should be:
    Take a photo, process it though the model. 
    Take the model result, and perform a collision check. 
        If a collision will happen by moving forward, call the 
        findBetterCourse() method, and send adjustments as needed. 
        
        If a collsion will not happen, move the drone a distance ahead, and start over. 

        Loop should be something like:
        TakePhoto()
        CheckIfCollision()
        AdjustCourse()
        Move()
    '''
    pass
        
if __name__ == '__main__':
    main()