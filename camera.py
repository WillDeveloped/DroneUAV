from djitellopy import tello
import cv2

drone = tello.Tello()
drone.connect()
drone.streamon()
STREAMING = True


while STREAMING:
    image = drone.get_frame_read().frame
    cv2.imshow("LIVE FEED", image)
    cv2.waitKey(1)

    