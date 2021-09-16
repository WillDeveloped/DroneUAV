import pygame 
import cv2
import numpy as np
import time
import pandas as pd

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


def mustMove(img):
  if (np.sum(img > INTENSITY) / (img.shape[0] * img.shape[1])) > MUSTMOVE:   
    return True
  else:
    return False

def getSections(img, direction = "none"):
  #Seperates the fov into 4 sections
  # [yMin:yMax, xMin, xMax]
  h, w = img.shape
  
  if direction == "none":
    img = img[h//3:h//3*2, :w]    #Should be middle third of screen
    #cv2_imshow(img)
    #print("MIDDLE ^ \n")
  if direction == "top":
    img = img[:h//3, :w]          #Should be top third of screen
    #cv2_imshow(img)
    #print("TOP ^ \n")
  if direction == "bot":
    img = img[h//3 * 2:, :w]      #Should be bottom third of screen
    #cv2_imshow(img)
    #print("BOTTOM ^ \n")

  img = img[:h//3, :w]
  sec1 = img[::, :w//4]           #First 4th
  sec2 = img[::, w//4 :w//4 *2]   #Second 4th
  sec3 = img[::, w//2 :w//4 *3]   #Third 4th
  sec4 = img[::, w//4 *3 :w]      #Forth 4th
  
  return [sec1, sec2, sec3, sec4] 

def determineMovement(img):
  
  top = []
  mid = []
  bot = []

  sec_top = getSections(img, "top")
  sec_mid = getSections(img)
  sec_bot = getSections(img, "bot")


  for section in sec_top:
    top.append(mustMove(section))

  for section in sec_mid:
    mid.append(mustMove(section))
    
  for section in sec_bot:
    bot.append(mustMove(section))

  Proceed = (np.sum(img > INTENSITY) / (img.shape[0] * img.shape[1])) < PROCEED  #If the sum of the pixels in the image are under the threshold, return true
  
  if not mid[1] and not mid[2] and Proceed:
    print("Move forward")

  if not top[1] and not top[2]:
    print("Can increase altitude and look again")
  #else:
    #print("Dont increase altitude")

  if not bot[1] and not bot[2]:
    print("Can decrease altitude and look again")
  #else:
    #print("Don't lower altitude")

  if mid[1] and not mid[0]:
    print("Can rotate ccw slightly and look again")
        
  if mid[2] and not mid[3]:
    print("Can rotate cw slightly and look again")

  #print("Rotate CCW / CW at least 90* and look again")
  print("")

def getInfo(img):
  #This just returns the information regarding pixels

  max = np.amax(img)
  min = np.amin(img)
  avg = np.average(img)
  percentOfMax = np.sum(img > INTENSITY) / (img.shape[0] * img.shape[1])

  print("Max:", max)
  print("Min:", min)
  print("Avg:", avg)
  print("Percent of > 200 intensity pixels", "{:.2f}".format(percentOfMax * 100))
  print(percentOfMax)
  print("\n")

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

    #if kb.isPressed("1"): drone.set_video_direction(tello.Tello.CAMERA_FORWARD)
    #elif kb.isPressed("2"): drone.set_video_direction(tello.Tello.CAMERA_DOWNWARD) 

    return[lr, fb, ud, yv]

def main():
    kb.init()
    
    drone = tello.Tello()
    drone.connect()
    
    #Settings for drone, initialize the telementry data
    drone.set_speed(10)
    response = drone.get_current_state()                        #Gets telementry data
    data = pd.DataFrame([response])                             #Creates dataframe of telementry data
    data.transpose()                                            #Sets up the dataframe correctly
  
    #drone.set_video_fps(tello.Tello.FPS_15)                     #lower than 15 and choppy, higher than 15 and it drops frames
    #drone.set_video_resolution(tello.Tello.RESOLUTION_480P)     #Sets resolution of video
    #drone.set_video_resolution(tello.Tello.RESOLUTION_720P)
    #drone.set_video_bitrate(tello.Tello.BITRATE_AUTO)          #Sets bitrate of stream
    

    drone.streamoff()                               #Resets the stream 
    drone.streamon()                                #starts the stream
    print("Battery:", drone.get_battery())
                            # MAIN LOOP #
    
    pft = time.time()
    fps = 0
    time.sleep(10)
    while True:
        img = drone.get_frame_read().frame
        
        #print("Shape of img from drone:", img.shape)
        nft = time.time()
        try:
            fps = 1/(nft - pft)
            pft = nft
            fps = int(fps)
            fps = str(fps)
        except:
            fps = 0

        #img = drone.get_frame_read().frame
        newResponse = drone.get_current_state()
        if img.shape == (720,960,3):
            img = classify(img)
            #determineMovement(img)
        cv2.putText(img, fps, (7,70), cv2.FONT_HERSHEY_SIMPLEX,  3, (255,255,255), 3, cv2.cv2.LINE_AA)
        cv2.imshow("LIVE FEED", img)
        cv2.waitKey(1)
        #print("Post Classification:", img.shape)
        
        velocity = getInput(drone)      #Gets input from drone

             #checks for change if nothing, keep going
        drone.send_rc_control(velocity[0], velocity[1], velocity[2], velocity[3])
               

        #image = monoDepth(drone.get_frame_read().frame)     #Sends the frame to the model. This gets hung up alot   
        #h, w, c = image.shape

        
        newResponse = drone.get_current_state()             
        
        #filename = "frames\\" + datetime.now().strftime('%H%M%S%f') + ".jpg"
        #cv2.imwrite(filename, img)
        data.loc[len(data)] = list(newResponse.values())    #appends to the dataframe           
        data.to_csv('gatheredData.csv', index=False)    
        
        
if __name__ == '__main__':
    main()