from datetime import datetime
import pygame 
import cv2
import numpy as np
import threading
import time
import pandas as pd

import keyboard as kb
from djitellopy import tello


techIssues = cv2.imread("images/technicalDifficulties.jpg")

def draw_area_of_concern(img, pitch):
    try:          
        h,w,c = img.shape
        if pitch < 0:
            pitch = pitch * -1
        cv2.rectangle(img, (0, h//3), (w,h//3 * 2 + pitch*2), (255,0,0), 4)
    except:
        return(techIssues)
    
    return(img)



def getInput(drone):
    
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 80
    
    if kb.isPressed("a"): lr = -speed
    elif kb.isPressed("d"): lr = speed

    if kb.isPressed("s"): fb = -speed
    elif kb.isPressed("w"): fb = speed

    if kb.isPressed("f"): ud = -speed
    elif kb.isPressed("r"): ud = speed

    if kb.isPressed("e"): yv = 100
    elif kb.isPressed("q"): yv = -100

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
    #drone.set_speed(100)
    response = drone.get_current_state()                        #Gets telementry data
    data = pd.DataFrame([response])                             #Creates dataframe of telementry data
    data.transpose()                                            #Sets up the dataframe correctly
  
    #drone.set_video_fps(tello.Tello.FPS_30)                     #lower than 15 and choppy, higher than 15 and it drops frames
    #drone.set_video_resolution(tello.Tello.RESOLUTION_480P)     #Sets resolution of video
    #drone.set_video_resolution(tello.Tello.RESOLUTION_720P)
    #drone.set_video_bitrate(tello.Tello.BITRATE_AUTO)          #Sets bitrate of stream
    #drone.set_video_direction(tello.Tello.CAMERA_FORWARD)

    drone.streamoff()                               #Resets the stream 
    drone.streamon()                                #starts the stream
    
                            # MAIN LOOP #
    print("Battery:", drone.get_battery())
    
    pft = time.time()
    num_frames = 1
    #cap = cv2.VideoCapture('udp://192.168.10.1:11111', cv2.CAP_FFMPEG)
    while True:        
        img = drone.get_frame_read().frame
        #newResponse = drone.get_current_state()
        #nft = time.time()
        #fps = 1/(nft - pft)
        #pft = nft
        #fps = int(fps)
        #fps = str(fps)
        #print(fps)
        #cv2.putText(img, fps, (7,70), cv2.FONT_HERSHEY_SIMPLEX,  3, (255,0,0), 3, cv2.cv2.LINE_AA)
        
        #draw_area_of_concern(img,newResponse["pitch"])
        cv2.imshow("LIVE FEED", img)
        cv2.waitKey(1)
        img = draw_area_of_concern(img, 0)
        velocity = getInput(drone)      #Gets input from drone
             #checks for change if nothing, keep going
        drone.send_rc_control(velocity[0], velocity[1], velocity[2], velocity[3])
        #image = monoDepth(drone.get_frame_read().frame)     #Sends the frame to the model. This gets hung up alot   
        #h, w, c = image.shape
    
        
        print("acc-x", drone.get_speed_x() , "acc-y", drone.get_speed_y(), "acc-z", drone.get_speed_z())
        #print("Velo-y", newResponse["vgy"]) 
        #print("Velo-z", newResponse["vgz"])

        #print("Acc-x", newResponse["agx"])
        #print("Acc-y", newResponse["agy"]) 
        #print("Acc-z", newResponse["agz"]) 
    
        
        #filename = "frames\\" + datetime.now().strftime('%H%M%S%f') + ".jpg"
        #cv2.imwrite(filename, img)
        #data.loc[len(data)] = list(newResponse.values())    #appends to the dataframe           
        #data.to_csv('gatheredData.csv', index=False)    
        
        
if __name__ == '__main__':
    main()