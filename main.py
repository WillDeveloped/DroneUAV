from datetime import datetime
import cv2
import numpy as np
import threading
import time
import pandas as pd
import keyboard as kb

from djitellopy import tello
from monoDepth import classify

velocity = [0, 0 ,0 ,0]

MUSTMOVE = .05
PROCEED = 0.50
INTENSITY = 200

techIssues = cv2.imread("images/technicalDifficulties.jpg")

def draw_area_of_concern(img, pitch):
    try:          
        h,w,c = img.shape
        cv2.rectangle(img, (0, h//3), (w,h//3 * 2 + pitch*2), (255,0,0), 4)
    except:
        pass  

def mustMove(img):
    if ((np.sum(img > INTENSITY) / (img.shape[0] * img.shape[1])) > MUSTMOVE):   
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

    Proceed = (img / (img.shape[0] * img.shape[1])) < PROCEED  

    #If the sum of the pixels in the image are under the threshold, return true
    
    
    
    print(Proceed, (img / (img.shape[0] * img.shape[1])), PROCEED)
    if not mid[1] and not mid[2] and Proceed:
        print("Move forward")
        #sendMovementCommands([0, 50, 0, 0], 10)
        return

    if not top[1] and not top[2]:
        print("Can increase altitude and look again")
        #sendMovementCommands([0, 0, 30, 0], 10)
        return
        #print("Can increase altitude and look again")
    #else:
        #print("Dont increase altitude")

    if not bot[1] and not bot[2]:
        print("Can decrease altitude and look again")
        #sendMovementCommands([0,0,20,0], 10)
        return
    #else:
        #print("Don't lower altitude")

    if mid[1] and not mid[0]:
        #sendMovementCommands([0,0,0,-100], 10)
        print("Can rotate ccw slightly and look again")
        return
        
            
    if mid[2] and not mid[3]:
        #sendMovementCommands([0,0,0,100], 10)
        print("Can rotate cw slightly and look again")
        return


    print("Rotate CCW / CW at least 90* and look again")
    
def avgFrame(img):
    #print("KMEANS CALLED")
    img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)        
    pixel_values = img.reshape((-1, 3))        
    pixel_values = np.float32(img)
    stopCritera = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)      
    k = 4

    _, labels, (centers) = cv2.kmeans(pixel_values, k, None, stopCritera, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    labels = labels.flatten()
    segmented_image = centers[labels.flatten()]
    segmented_image = segmented_image.reshape(img.shape)

    #print("img kmeansed")
    img = cv2.resize(img, (0,0), fx=2, fy=2)
    return img

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

def sendMovementCommands(velocity, itterations):
    
    lr, fb, ud, yaw = velocity 

    for x in range(0, itterations):
        drone.send_rc_control(lr, fb, ud, yaw)
        time.sleep(.01)    


def main():
    kb.init()
    global drone
    drone = tello.Tello()
    drone.connect()
    
    drone.set_speed(10)
    response = drone.get_current_state()                        #Gets telementry data
    data = pd.DataFrame([response])                             #Creates dataframe of telementry data
    data.transpose()                                            #Sets up the dataframe correctly

    drone.set_video_fps(tello.Tello.FPS_15)                     #lower than 15 and choppy, higher than 15 and it drops frames
    drone.set_video_resolution(tello.Tello.RESOLUTION_720P)
    drone.set_video_bitrate(tello.Tello.BITRATE_5MBPS)          #Sets bitrate of stream
    
    drone.streamoff()                               #Resets the stream 
    drone.streamon()                                #starts the stream
    
                            # MAIN LOOP #
    while True:

        #telemetry = drone.get_current_state()

        img = drone.get_frame_read().frame
        
        img = classify(img)
        
        img = avgFrame(img)
        
        print(img.shape)

        velocity = getInput(drone)

        determineMovement(img)


        time.sleep(.25)

        #cv2.imshow("LIVE FEED", img)
        #cv2.waitKey(1)
        
        #velocity = getInput(drone)      #Gets input from drone  Needs to be fixed

        #drone.send_rc_control(velocity[0], velocity[1], velocity[2], velocity[3])
        
        #filename = "frames\\" + datetime.now().strftime('%H%M%S%f') + ".jpg"
        #cv2.imwrite(filename, img)
        
if __name__ == '__main__':
    main()