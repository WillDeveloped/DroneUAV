import cv2
import numpy as np
import threading
import time
import pandas as pd
from djitellopy import tello


def getTelemetry(runTime, direction):               #Runtime is a time in seconds that the operation should take, direction is the command called
    response = drone.get_current_state()            #Gets dict response
    data = pd.DataFrame([response])                 #Creates data frame
    data.transpose()
    data['time'] = time.time()                      #adds the time column
        
    for x in range(1, runTime * 10):                #10 would need to be changed according to what you sleep for at the end of the loop
        newResponse = drone.get_current_state()
        data.loc[x] = list(newResponse.values())    #appends to the dataframe
        time.sleep(.1)

    fileName = direction + str(runTime) + '.csv'
    data.to_csv(fileName, index=False)
    print(fileName, "added")


def move():
    drone.connect()
    getTelemetry(10, 'forward')
    drone.takeoff()
    drone.set_speed(10) #~4 inches or 10 cm/s
    
    for x in range(100):
        velocity = [0,100,0,0]
        drone.send_rc_control(velocity)
        time.sleep(.1)

    drone.land()


if __name__ == '__main__':
    drone = tello.Tello()
    drone.connect()
    move()
