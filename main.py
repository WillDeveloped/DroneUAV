import pygame 
import cv2
import numpy as np
import threading
import time
import pandas as pd

import keyboard as kb
from djitellopy import tello
from monoDepth import monoDepth


velocity = [0, 0 ,0 ,0]
#programed as lr, fb, y, t 
#lr is left right
#fb is front back
#y is yaw
#t is throttle

def getInput(drone):
    
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

    if kb.isPressed("m"): drone.turn_motor_on 
    elif kb.isPressed("n"): drone.turn_motor_off

    if kb.isPressed("t"): drone.takeoff()
    elif kb.isPressed("l"): drone.land()

    return[lr, fb, ud, yv]

def main():
    kb.init()
    oldVelocity = [0,0,0,0]
    drone = tello.Tello()
    drone.connect()
    
    #Settings for drone, initialize the telementry data
    drone.set_speed(10)
    response = drone.get_current_state()                        #Gets telementry data
    data = pd.DataFrame([response])                             #Creates dataframe of telementry data
    data.transpose()                                            #Sets up the dataframe correctly
  
    drone.set_video_fps(tello.Tello.FPS_15)                     #lower than 15 and choppy, higher than 15 and it drops
    drone.set_video_resolution(tello.Tello.RESOLUTION_480P)     #Sets resolution of video
    #drone.set_video_resolution(tello.Tello.RESOLUTION_720P)
    drone.set_video_bitrate(tello.Tello.BITRATE_5MBPS)
    

    drone.streamoff()                               #Resets the stream 
    drone.streamon()
    while True:
        velocity = getInput(drone)

        if oldVelocity != velocity:
            drone.send_rc_control(velocity[0], velocity[1], velocity[2], velocity[3])
        oldVelocity = velocity

        image = monoDepth(drone.get_frame_read().frame)
        newResponse = drone.get_current_state()
                         
        cv2.imshow("LIVE FEED", image)
        cv2.waitKey(1)

        data.loc[len(data)] = list(newResponse.values())    #appends to the dataframe           
        data.to_csv('gatheredData.csv', index=False)    
        
        
if __name__ == '__main__':
    main()