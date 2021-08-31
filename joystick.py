import pygame

dead_zone = 0.09 #Change this so that the inputs only change if an inteneded velocity change takes place
velocity = [0.0, 0.0 ,0.0 ,0.0]
#programed as lr, fb, y, t 
#lr is left right
#fb is front back
#y is yaw
#t is throttle

def init():
    pygame.init()
    window = pygame.display.set_mode((250,250))
    global j0 
    j0 = pygame.joystick.Joystick(0)
    j0.init()


def getJoystickInput():
    global velocity
    
    for eve in pygame.event.get(): pass
        
       
    for x in range(0,4):
        if abs(j0.get_axis(x)) < dead_zone:
            velocity[x] = 0.0
        else:
            velocity[x] = int(100 * j0.get_axis(x))  
        
def main():
    getJoystickInput()

    print(velocity)

if __name__ == '__main__':
    init()
    while True:
        main()


'''
if eve.type == pygame.KEYDOWN:
           if eve.key == pygame.K_ESCAPE:
               print("****  Drone Landing  ****")
               drone.land()
               drone.streamoff()
               time.time.sleep(3)
               STREAMING = False
           if eve.key == pygame.K_t:
                print("**** Drone Taking off ****")
                drone.takeoff()
                time.time.sleep(3)
                DEPLOYED = True


 
 
        if eve.type == pygame.KEYDOWN and eve.key == pygame.K_ESCAPE:
            print("*** DRONE LANDING ***")
            print(velocity)
            #call drone.land(), drone.streamoff(), time.time.sleep(3)
            #set STREAMING = False
        if eve.type == pygame.KEYDOWN and eve.key == pygame.K_t:
            print("****  DRONE TAKING OFF  ****")
            print(velocity)
            #drone.takeoff(), 
            #DEPLOYED = True
        

'''