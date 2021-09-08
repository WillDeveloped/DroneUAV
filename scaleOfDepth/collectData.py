import cv2
import numpy as np
import pandas as pd
import os

distance = 120
distances = []
pixelIntensity = []

DIR='images'

x = 1160
y = 330
w = 1400 - x
h =  655 - y

for root, dirs, files in os.walk(DIR):
    for name in files:
        print("Starting with:", name)
        img = cv2.imread("images//" + name)
        print(img.shape)
        mask = np.zeros(img.shape, np.uint8)
        mask[y:y+h, x:x+w] = img[y:y+h, x:x+w]
        pixelIntensity.append(np.amax(mask))
        distances.append(distance)
        distance = distance + 10

data = pd.DataFrame(list(zip(distances, pixelIntensity)))

data.to_csv('data.csv')