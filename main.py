import pygame 
import cv2
import numpy as np
import threading
import time


import keyboard as kb
from djitellopy import tello


velocity = [0, 0 ,0 ,0]
#programed as lr, fb, y, t 
#lr is left right
#fb is front back
#y is yaw
#t is throttle

drone = tello.Tello()
drone.connect()

#print("SDK VERSION")
#drone.query_sdk_version()
#print("serial number")
#drone.query_serial_number()
drone.set_video_fps(tello.Tello.FPS_30) 
drone.set_video_resolution(tello.Tello.RESOLUTION_720P)
drone.set_video_bitrate(tello.Tello.BITRATE_5MBPS)
drone.streamon()

    
#print("[INFO] Joystick connected")
print("[INFO] DRONE CONNECTED")
print("[INFO] LIVE FEED CONNECTED")
    
def getStream():
    while True:
        image = drone.get_frame_read().frame
        cv2.imshow("LIVE FEED", image)
        cv2.waitKey(1)


def getInput():

    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 60

    if kb.getInput("a"): lr = -speed
    if kb.getInput("d"): lr = speed

    if kb.getInput("s"): fb = -speed
    if kb.getInput("w"): fb = speed

    if kb.getInput("f"): ud = -speed
    if kb.getInput("r"): ud = speed

    if kb.getInput("e"): yv = -speed
    if kb.getInput("q"): yv = speed

    if kb.getInput("t"): drone.takeoff()
    if kb.getInput("l"): drone.land()

    return[lr, fb, ud, yv]


def main():
    liveFeed = threading.Thread(target=getStream, args=())
    liveFeed.start()

    while True:
        velocity = getInput()
        drone.send_rc_control(velocity[0], velocity[1], velocity[2], velocity[3])
        

if __name__ == '__main__':
    main()