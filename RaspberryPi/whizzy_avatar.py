import os
import time
import pygame
import threading
from textwrap import wrap
from text_to_speech import gtts_speak

talking = False
screen = None
handler = None
mic_flag = False
small = False

white = (255, 255, 255)
yellow = (255, 255, 0)
width, height = 400, 70

mode_text = ''
subtitle_list = []
subtitle_phrase = ''
lesson_text = 'Lesson: Please load a lesson'

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
    global talking
    
    A = 0
    B = 0
    x = 1920
    y = 1080

    count = 1
    while True:
        pygame.event.get()
        if talking == False:
            handler.render(screen, "1", (A, B), True, (x, y))
            display_text()
            time.sleep(0.3)

        elif talking == True:
            if count <= 2:
                count += 1
            img = str(count)
            
            handler.render(screen, img, (A, B), True, (x, y))
            display_text()
            time.sleep(0.3)
            
            count += 1
            if count == 8:
                count = 2
        
        pygame.display.update(A, B, x, y)
        
# displays text
def display_text():    
    #display current mode
    font = pygame.font.Font('avatar/comicsans.TTF', 35, bold= True)
    mode_text_render = font.render(mode_text, True, white)
    text_width = mode_text_render.get_width()
    
    x, y = 100, 90
    pygame.draw.rect(screen, white, (x, y, text_width+50, height+10), 3, 10)  # rectangle
    screen.blit(mode_text_render, (x+23, y+12, width, height))  # text
    
    if 'Interactive Discussion' in mode_text:
        #display current lesson
        lesson_text_render = font.render(lesson_text, True, white)
        text_width = lesson_text_render.get_width()
        
        x_2,y_2 = 1920-(text_width+150), 90
        pygame.draw.rect(screen, white, (x_2, y_2, text_width+50, height+10), 3, 10)  # rectangle
        screen.blit(lesson_text_render, (x_2+23, y_2+12, width, height))  # text
        
    mic()
    display_subtitle()
    pygame.display.flip()

def subtitle():
    global subtitle_phrase, subtitle_list, talking
    
    while True:
        if len(subtitle_list) != 0:
            set_avatar_state(True)
            
            for phrase in subtitle_list:
                subtitle_phrase = phrase
                gtts_speak(phrase)
                
            subtitle_phrase = ''
            subtitle_list = []
            set_avatar_state(False)
            
def display_subtitle():
    font = pygame.font.Font('avatar/comicsans.TTF', 35, bold= True)
    
    if subtitle_phrase != '':
        subtitle_text_render = font.render(subtitle_phrase, True, white)
        text_width = subtitle_text_render.get_width()
        
        available_space = 1920 - text_width
        x_value = available_space / 2    
        screen.blit(subtitle_text_render, (x_value, 1020, width, height))
        
def mic():
    global small
    coordinate = (150, 1080-125)
    
    #display circle
    if mic_flag is True and small is True:
        pygame.draw.circle(screen, yellow, coordinate, 80, 100)
        small = False
        
    elif mic_flag is True and small is False:
        pygame.draw.circle(screen, yellow, coordinate, 95, 100)
        small = True
        
    else:
        pygame.draw.circle(screen, white, coordinate, 80, 100)
    
    #display image
    mic_img = pygame.image.load('avatar/mic.bmp').convert_alpha()
    mic_img = pygame.transform.scale(mic_img, (64, 109.5))
    screen.blit(mic_img, (120, 902))

def whizzy_speak(text):
    global subtitle_list
    
    list_of_phrases = wrap(text,90)
    subtitle_list = list_of_phrases
    
    while len(subtitle_list) != 0:
        continue
    
def set_mic_state(mic_state):
    global mic_flag
    mic_flag = mic_state
    
def set_avatar_state(avatar_state):
    global talking
    talking = avatar_state
    
def get_avatar_state():
    return talking

def set_mode_text(text):
    global mode_text
    mode_text = f'Mode: {text.title()}'

def set_lesson_text(text):
    global lesson_text
    lesson_text = f'Lesson: {text}'
    
def initialize_avatar():
    global screen, handler
    
    #initialize display
    pygame.display.init()  # Initiates the display pygame
    pygame.font.init()
    pygame.display.set_caption("Whizzy")
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)  # allows fullscreen
    handler = imageHandler()
    
    display()
    threading.Thread(target=face, daemon=True).start()
    subtitle()