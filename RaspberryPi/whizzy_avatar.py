from __future__ import print_function

#hide pygame import message
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

import time

talking = False
screen = None
handler = None

class imageHandler:
    def __init__(self):
        self.pics = dict()

    def loadFromFile(self, filename, id=None):
        if id == None: id = filename
        self.pics[id] = pygame.image.load(filename).convert()

    def loadFromSurface(self, surface, id):
        self.pics[id] = surface.convert_alpha()

    def render(self, surface, id, position=None, clear=False, size=None):
        if clear == True:
            surface.fill((5, 2, 23))  #

        if position == None:
            picX = int(surface.get_width() / 2 - self.pics[id].get_width() / 2)
        else:
            picX = position[0]
            picY = position[1]

        if size == None:
            surface.blit(self.pics[id], (picX, picY))  #

        else:
            surface.blit(pygame.transform.smoothscale(self.pics[id], size), (picX, picY))
            
#pass new avatar talking state
def change_avatar_state(avatar_state):
    global talking
    talking = avatar_state

#images
def display():
    #not talking
    handler.loadFromFile("avatar/1.bmp", "1")

    #talking
    handler.loadFromFile("avatar/2.bmp", "2")
    handler.loadFromFile("avatar/3.bmp", "3")
    handler.loadFromFile("avatar/4.bmp", "4")
    handler.loadFromFile("avatar/5.bmp", "5")
    handler.loadFromFile("avatar/6.bmp", "6")
    handler.loadFromFile("avatar/7.bmp", "7")
    handler.loadFromFile("avatar/8.bmp", "8")

def face():
    A = 0
    B = 0
    x = 1920 #width
    y = 1080 #length
    
    count = 1
    global talking
    while True:
        pygame.event.get()
        if talking == False:
            handler.render(screen, "1", (A, B), True, (x, y))
            pygame.display.update(A, B, x, y)


        elif talking == True:
            if count <= 2:
                count += 1
            img = str(count)
            handler.render(screen, img, (A, B), True, (x, y))
            pygame.display.update(A, B, x, y)
            time.sleep(0.3)
            count += 1
            if count == 8:
                count = 2
                
def initialize_avatar():
    global screen, handler
    
    #initialize display
    pygame.display.init()  # Initiates the display pygame
    pygame.display.set_caption("Whizzy")
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)  # allows fullscreen
    handler = imageHandler()
    
    display()         
    face()