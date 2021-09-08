import pygame 
import cv2
import numpy as np
import threading
import time


import keyboard as kb
from djitellopy import Tello


velocity = [0, 0 ,0 ,0]
#programed as lr, fb, y, t 
#lr is left right
#fb is front back
#y is yaw
#t is throttle

kb.init()
drone = Tello()
drone.connect()
#drone.set_video_fps(drone.Tello.FPS_30) 
#drone.set_video_resolution(drone.Tello.RESOLUTION_720P)
#drone.set_video_bitrate(drone.Tello.BITRATE_5MBPS)
drone.streamon()


def getStream():
    '''
    Still need to pipe the video feed to the prediction model.
    
    tello.py has a method "get_video_capture" 
    that returns a VideoCapture (Might be good)
    
    '''

    while True:
        image = drone.get_frame_read().frame
        cv2.imshow("LIVE FEED", image)
        cv2.waitKey(1)


def getInput():
    
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 60

    if kb.isPressed("a"): lr = -speed//2
    elif kb.isPressed("d"): lr = speed//2

    if kb.isPressed("s"): fb = -speed
    elif kb.isPressed("w"): fb = speed

    if kb.isPressed("f"): ud = -speed
    elif kb.isPressed("r"): ud = speed

    if kb.isPressed("e"): yv = speed
    elif kb.isPressed("q"): yv = -speed

    if kb.isPressed("t"): drone.takeoff()
    elif kb.isPressed("l"): drone.land()

    return[lr, fb, ud, yv]


def main():
    liveFeed = threading.Thread(target=getStream, args=())
    liveFeed.start()
    prev_velocity = [0,0,0,0]
    while True:
        velocity = getInput()    
        if prev_velocity != velocity:
            drone.send_rc_control(velocity[0], velocity[1], velocity[2], velocity[3])
        prev_velocity = velocity

if __name__ == '__main__':
    main()