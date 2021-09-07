import pygame

def init():
    pygame.init()
    win = pygame.display.set_mode((250,250))

def getInput(keyboardInput):
    res = False
    for eve in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    key = getattr(pygame, 'K_{}'.format(keyboardInput))
    if KeyboardInterrupt[key]:
        res = True
    pygame.display.update()
    return res

if __name__ =='__main__':
    init()