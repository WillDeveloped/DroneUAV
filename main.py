import pygame 
import cv2
import numpy as np
import threading
import time


from djitellopy import tello

#VARIABLES
S = .6                  #Speed of the drone. Max is 1

dead_zone = 0.09        #Change this so that the inputs only change 
                        #if an inteneded velocity change takes place

velocity = [0, 0 ,0 ,0]
#programed as lr, fb, y, t 
#lr is left right
#fb is front back
#y is yaw
#t is throttle


def init():
    global j0
    global drone
    global STREAMING
    pygame.init()
    window = pygame.display.set_mode((250,250))
    j0 = pygame.joystick.Joystick(0)
    j0.init()
    drone = tello.Tello()
    drone.connect()
    drone.set_video_fps("Tello.FPS_30")
    drone.set_video_resolution("Tello.RESOLUTION_720P")
    drone.set_video_bitrate("Tello.BITRATE_5MBPS")
    drone.streamon()
    STREAMING = True
    
    print("[INFO] Joystick connected")
    print("[INFO] DRONE CONNECTED")
    print("[INFO] LIVE FEED CONNECTED")
    
def getStream():
    global drone
    image = drone.get_frame_read().frame
    cv2.imshow("LIVE FEED", image)
    cv2.waitKey(1)

    while STREAMING:
        image = drone.get_frame_read().frame
        cv2.imshow("LIVE FEED", image)
        cv2.waitKey(1)

def getJoystickInput():
    global velocity
    global dead_zone
    global drone
    global STREAMING
    global DEPLOYED
    for eve in pygame.event.get():
        if eve.type == pygame.KEYDOWN:
            if eve.key == pygame.K_ESCAPE:
                print("****  Drone Landing  ****")
                drone.land()
                drone.streamoff()
                time.time.sleep(3)
                STREAMING = False
            if eve.key == pygame.K_t:
                print("**** Drone Taking off ****")
                drone.takeoff()
                time.time.sleep(3)
                DEPLOYED = True
    
    for x in range(0,4):
        if abs(j0.get_axis(x)) < dead_zone:
            velocity[x] = 0
        else:
            velocity[x] = int(100  * j0.get_axis(x))
    
def main():
    controls = threading.Thread(target=getJoystickInput, args=())
    liveFeed = threading.Thread(target=getStream, args=())
    controls.start()
    liveFeed.start()

    while DEPLOYED:
        drone.send_rc_control(velocity[0], velocity[1], int(velocity[3]*S) , velocity[2])

if __name__ == '__main__':
    init()
    main()