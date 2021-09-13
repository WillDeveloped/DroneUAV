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

whT = 320
confidence_threshold = 0.5
nmsThreshold = 0.3
classesFile = 'Resources\Yolo\coco.names'
classNames = [classesFile]

with open(classesFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

modelConfig = 'Resources\Yolo\yolov3-tiny.cfg'
modelWeights = 'Resources\Yolo\yolov3-tiny.weights'

net = cv2.dnn.readNetFromDarknet(modelConfig, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


def findObjects(outputs, img):
    hT, wT, cT = img.shape
    boundingBox = []
    classIds = []
    confs = []

    for output in outputs:
        for det in output:
            scores = det[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            if confidence > confidence_threshold:
                w,h = int(det[2]*wT), int(det[3]*hT)
                x,y = int((det[0]*wT) - w/2), int((det[1]*hT)-h/2)
                boundingBox.append([x,y,w,h])
                classIds.append(classID)
                confs.append(float(confidence))


    indices = cv2.dnn.NMSBoxes(boundingBox, confs, confidence_threshold, nmsThreshold)

    for i in indices:
        i = i[0]
        box = boundingBox[i]
        x,y,w,h = box[0], box[1], box[2], box[3]
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,255), 2)
        cv2.putText(img, f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%', (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,255), 2)




def getInput(drone):
    
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 75
    
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
    drone.set_video_fps(tello.Tello.FPS_15)
    drone.set_video_resolution(tello.Tello.RESOLUTION_480P)
    drone.set_video_bitrate(tello.Tello.BITRATE_5MBPS)
    print("Battery:", drone.get_battery())
    
    #Settings for drone, initialize the telementry data
    drone.set_speed(10)
    #response = drone.get_current_state()                        #Gets telementry data
    #data = pd.DataFrame([response])                             #Creates dataframe of telementry data
    #data.transpose()                                            #Sets up the dataframe correctly   

    drone.streamoff()                               #Resets the stream 
    drone.streamon()

    cap = cv2.VideoCapture('udp://0.0.0.0:11111')

    
    while True:

        velocity = getInput(drone)

        if oldVelocity != velocity:                 #Only send a new command if the values have changed
            drone.send_rc_control(velocity[0], velocity[1], velocity[2], velocity[3])
        oldVelocity = velocity      
        
        success, img = cap.read()
        blob = cv2.dnn.blobFromImage(img, 1/255, (whT, whT), [0,0,0], 1, crop=False)
        net.setInput(blob)
        layerNames = net.getLayerNames()
        #print(layerNames)
        outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]
        outputs = net.forward(outputNames)
        #print(len(outputs).shape)
        findObjects(outputs,img)

        cv2.imshow('image', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
                      
        
    
        
        
if __name__ == '__main__':
    main()