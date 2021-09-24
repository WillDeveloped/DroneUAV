import pygame 
import cv2
import numpy as np
import time
import pandas as pd
import math
import datetime

import keyboard as kb
from djitellopy import tello
from monoDepth import classify

#This may not be needed anymore. Might be switching to 
#Move commands that wait for a response

velocity = [0, 0 ,0 ,0]
#programed as lr, fb, y, t 
#lr is left right
#fb is front back
#y is yaw
#t is throttle
MUSTMOVE = .15
PROCEED = 0.60
INTENSITY = 180


def avgFrame(img):

    img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
    pixel_values = img.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)
    stopCritera = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    k = 3
    _, labels, (centers) = cv2.kmeans(pixel_values, k, None, stopCritera, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
 
    labels = labels.flatten()
    segmented_image = centers[labels.flatten()]
    segmented_image = segmented_image.reshape(img.shape)

    segmented_image = cv2.resize(img, (0,0), fx=2, fy=2)
    return segmented_image, centers


def calculateDistance(x1, x2, y1, y2):
  dist = math.sqrt( (x2-x1)**2 + (y2-y1)**2)
  return int(dist)


def getMovementVector(img):
  
  img, centers = avgFrame(img)
  darkest_px = np.where(img <= np.amin(centers))
  
  if len(darkest_px[0]) < 1 and len(darkest_px[1]) < 1:
    return 0,0,0,img
   
  ty = int(sum(darkest_px[0])/len(darkest_px[0]))
  tx = int(sum(darkest_px[1])/len(darkest_px[1]))

  originx = int(img.shape[1]/2)
  originy = int(img.shape[0]/2)

  x_comp = int((tx - originx)/720 * 100)
  y_comp = int((originy - ty)/360 * 100)
  mag = int(calculateDistance(originx, tx, originy, ty)/788 * 100)

  #cv2.circle(img, (tx,ty), 10,(0), -1) #This draws the circle on the image to see where on the image the vector is going to take the drone
  
  #These lines draw the visuals on the image. Comment them out unless trouble shooting.
  
  shp1 = img.shape[1]
  shp0 = img.shape[0]
  
  img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
  cv2.circle(img, (tx,ty), 10,(0), -1) #This draws the circle on the image to see where on the image the vector is going to take the drone
  
  startpoint = (int(shp1/2), 0)
  endpoint =  (int(shp1/2), shp0)
  cv2.line(img, startpoint, endpoint, (0,0,255), 3)
  startpoint = (0,int(shp0/2))
  endpoint = (shp1, int(shp0/2))
  cv2.line(img, startpoint, endpoint, (0,0,255), 3)
  
  cv2.circle(img, (originx,originy), 2,(0), -1)
  cv2.line(img, (originx, originy), (tx, ty), (255,0,0), 3)
  cv2.line(img, (tx, ty), (tx, originy),  (255,0,255), 3)    #Y Comp
  cv2.putText(img, "Y COMP:" + str(originy - ty), (1000, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2)
  cv2.line(img, (originx, originy), (tx, originy),  (255,0,255), 3) # X Comp
  cv2.putText(img, "X COMP:" + str(tx - originx), (1000, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2)
  cv2.putText(img, "Mag:" + str(calculateDistance(originx, tx, originy, ty)), (1000, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2)

  
  print(x_comp, y_comp, mag)
  return x_comp, y_comp, mag, img


def getInput(drone):
    #Only here for reference
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

    #if kb.isPressed("1"): drone.set_video_direction(tello.Tello.CAMERA_FORWARD)
    #elif kb.isPressed("2"): drone.set_video_direction(tello.Tello.CAMERA_DOWNWARD) 

    return[lr, fb, ud, yv]

def main():
    kb.init()
    
    drone = tello.Tello()
    drone.connect()
    img = cv2.imread("images/initialize.png")       #Initializes the model
    img = classify(img)
    
    #Settings for drone, initialize the telementry data
    #drone.set_speed(10)
    #response = drone.get_current_state()                        #Gets telementry data
    #data = pd.DataFrame([response])                             #Creates dataframe of telementry data
    #data.transpose()                                            #Sets up the dataframe correctly
  
    #drone.set_video_fps(tello.Tello.FPS_15)                     #lower than 15 and choppy, higher than 15 and it drops frames
    #drone.set_video_resolution(tello.Tello.RESOLUTION_480P)     #Sets resolution of video
    #drone.set_video_resolution(tello.Tello.RESOLUTION_720P)
    #drone.set_video_bitrate(tello.Tello.BITRATE_AUTO)          #Sets bitrate of stream
    
 
    drone.streamoff()                               #Resets the stream 
    drone.streamon()                                #starts the stream
    print("Battery:", drone.get_battery())
                            
                            
                            
                            # MAIN LOOP #
    
    #pft = time.time()
    #fps = 0
    #time.sleep(10)
    while True:
        img = drone.get_frame_read().frame
        
       
        #nft = time.time()
        #try:
        #    fps = 1/(nft - pft)
        #    pft = nft
        #    fps = int(fps)
        #    fps = str(fps)
        #except:
        #    fps = 0

        #newResponse = drone.get_current_state()
        if img.shape == (720,960,3):
            img = classify(img)
            x_comp, y_comp, mag, img = getMovementVector(img)
            #img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        #cv2.putText(img, fps, (7,70), cv2.FONT_HERSHEY_SIMPLEX,  3, (255,255,255), 3, cv2.cv2.LINE_AA)
        cv2.imshow("LIVE FEED", img)
        cv2.waitKey(1)
        #print("Post Classification:", img.shape)
        
        velocity = getInput(drone)      #Gets input from drone
        drone.send_rc_control(velocity[0], velocity[1], velocity[2], velocity[3])             
        
        #filename = "frames\\" + datetime.now().strftime('%H%M%S%f') + ".jpg"
        #cv2.imwrite(filename, img)
        #data.loc[len(data)] = list(newResponse.values())    #appends to the dataframe           
        #data.to_csv('gatheredData.csv', index=False)    
        
        
if __name__ == '__main__':
    main()