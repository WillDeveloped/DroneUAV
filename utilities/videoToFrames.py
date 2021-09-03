import cv2


vidcap = cv2.VideoCapture('droneTestFootage.mp4')
success, image = vidcap.read()
print(success)
count = 0
while success:
    cv2.imwrite("../Resources/pictures/frame%d.jpg" % count, image) # save frame as JPEG file.
    success,image = vidcap.read()
    print('Read a new frame: ', success)
    count += 1


print(count)