from djitellopy import tello

drone = tello.Tello()
drone.connect()


FPS = "Tello.FPS_30"
RESOLUTION = "Tello.RESOLUTION_720P"
BITRATE = "Tello.BITRATE_5MBPS"


print("SDK VERSION")
drone.query_sdk_version()

print("serial number")
drone.query_serial_number()

#print("Setting connection settings", FPS, RESOLUTION, BITRATE )
drone.set_video_fps(tello.Tello.FPS_30) 
drone.set_video_resolution(tello.Tello.RESOLUTION_720P)
drone.set_video_bitrate(tello.Tello.BITRATE_5MBPS)

#drone.turn_motor_on()