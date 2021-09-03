from djitellopy import tello

drone = tello.Tello()
drone.connect()
print("SDK VERSION")
drone.query_sdk_version()

print("serial number")
drone.query_serial_number()