import os
import numpy as np
import cv2
import glob


def convertToVideo():
    img_array = []
    directory = sorted(glob.glob('../Mono_Depth/output/*.png'))

    print(directory)

    #for filename in directory:
        #print(filename)

    '''
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    
    out = cv2.VideoWriter('splicedVideo.avi',cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
    
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

    '''
if __name__ == '__main__':
    convertToVideo()
