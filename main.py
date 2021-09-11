import pygame 
import cv2
import numpy as np
import threading
import time
import pandas as pd

import keyboard as kb
from djitellopy import tello


velocity = [0, 0 ,0 ,0]
#programed as lr, fb, y, t 
#lr is left right
#fb is front back
#y is yaw
#t is throttle

kb.init()
drone = tello.Tello()
drone.connect()
#drone.set_video_fps(drone.Tello.FPS_30) 
#drone.set_video_resolution(drone.Tello.RESOLUTION_720P)
#drone.set_video_bitrate(drone.Tello.BITRATE_5MBPS)
#drone.streamon()


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


def getTelemetry(data):
        newResponse = drone.get_current_state()
        data.loc[len(data)] = list(newResponse.values())    #appends to the dataframe           
        data.to_csv('gatheredData.csv', index=False)
        


def getInput():
    
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 60

    if kb.isPressed("a"): lr = -speed
    elif kb.isPressed("d"): lr = speed

    if kb.isPressed("s"): fb = -speed
    elif kb.isPressed("w"): fb = speed

    if kb.isPressed("f"): ud = -speed
    elif kb.isPressed("r"): ud = speed

    if kb.isPressed("e"): yv = speed
    elif kb.isPressed("q"): yv = -speed

    if kb.isPressed("t"): 
        drone.takeoff()
        time.sleep(3)
    elif kb.isPressed("l"): drone.land()

    return[lr, fb, ud, yv]


def main():
    #liveFeed = threading.Thread(target=getStream, args=())
    #liveFeed.start()

    #getTele = threading.Thread(target=getTelemetry, args=(10, 'forward'))
    #getTele.start()
    drone.set_speed(10)
    response = drone.get_current_state()            #Gets dict response
    data = pd.DataFrame([response])                 #Creates data frame
    data.transpose()
    
    
    
    while True:
        velocity = getInput()    
        drone.send_rc_control(velocity[0], velocity[1], velocity[2], velocity[3])
        getTelemetry(data)
        time.sleep(.2)
    

if __name__ == '__main__':
    main()