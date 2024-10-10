import os
import pygame
from pygame.locals import *
#from time import time

from datetime import datetime

clock = pygame.time.Clock()

pygame.init()

screen = pygame.display.set_mode((800,600), HWSURFACE | DOUBLEBUF | RESIZABLE)
 
pygame.display.set_caption("Золупка")

icon = pygame.image.load('icon.png')

bg = pygame.image.load('bg.jpg')


img = pygame.image.load('gif.gif')

pygame.display.set_icon(icon)

running = True
screen.fill((100,200,100))

square = pygame.Surface((100,100))
square.fill('Blue')

base_timer = 10
timer_ = base_timer
myfont = pygame.font.Font('AmaticSC.ttf' , 40)
gmyfont = pygame.font.Font('AmaticSC.ttf' , 60)

gamover = myfont.render('Game Over!', True, 'red') 

time_now = datetime.now()

while running:
    
    if ((datetime.now() - time_now).total_seconds() >=1):
        if timer_ != 0:
            timer_ = timer_-1
        time_now = datetime.now()
        
    text_surface = myfont.render(str(timer_), True, 'white')
    
    clock.tick(10)
    screen.blit(bg,(0,0))
    screen.blit(text_surface,(50,50))

    if timer_ == 0:
        screen.blit(gamover,(100,100))
    #screen.draw.rect()
    
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            timer_ = base_timer
            #pos = pygame.mouse.get_pos()
            #clicked_ = [s for s in sprites if s.rect.collidepoint(pos)]
            #print(pos)
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
'''
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                screen.fill((200,200,100))
            
''' 



