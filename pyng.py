import pygame, sys, os
from pygame.locals import *

full_path = os.path.realpath(__file__)
path, file = os.path.split(full_path)

import states


#put the state manager in the begining state
states.manager.Switch(2)

#init py game and counter for fps
pygame.init()
fpsClock = pygame.time.Clock()

#create window and main surface
windowSurfaceObj = pygame.display.set_mode((800,600))
pygame.display.set_caption('Pyng')

#load sound
soundObj = pygame.mixer.Sound(path + '\\bounce.wav')

#main loop
while True:

    #loop
    states.manager.stateArray[states.manager.current].loop()

    #render
    states.manager.stateArray[states.manager.current].render(windowSurfaceObj)

    #events
    for event in pygame.event.get():
        states.manager.stateArray[states.manager.current].event(event)

    pygame.display.update()
    fpsClock.tick(30)
