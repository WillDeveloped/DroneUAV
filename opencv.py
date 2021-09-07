import cv2
from djitellopy import Tello
import asyncio
from tello_asyncio import VIDEO_URL
import numpy as np


drone = Tello()
drone.connect()
drone.streamon()
drone.turn_motor_on()

#cap = drone.get_frame_read().frame

cap = cv2.VideoCapture(VIDEO_URL)
        
#print("Drone feed is of type", cap)
#print("Webcam feed is of type",img)


whT = 320
confidence_threshold = 0.5
nmsThreshold = 0.3
classesFile = 'Resources\Yolo\coco.names'
classNames = []

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


while True:
    success, img = cap.read()
    blob = cv2.dnn.blobFromImage(img, 1/255, (whT, whT), [0,0,0], 1, crop=False)
    net.setInput(blob)
    layerNames = net.getLayerNames()
    #print(layerNames)
    outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(outputNames)
    #print(len(outputs).shape)
    findObjects(outputs,img)
    

    '''
    
    outputs:
        (300,85)        produces 300 bounding boxes
        (1200, 85)      1200 bounding boxes
        (4800, 85)      4800 bounding boxes

        the 85. first 5 values, center x, center y, width, height, confidence
        the other 81 are the probability that the key value pair is in the box. 
        so object 1 is person. the value is the percentage of confidence
        that there's a person in the bounding box. 
    
    '''

    cv2.imshow('image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

