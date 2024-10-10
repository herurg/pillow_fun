import pygame as pg
import os
from pygame.locals import *
import serial
from time import sleep


#Open Art SDXL


serial_on = True
try:
    ser = serial.Serial("COM11", 115200)
except:
    serial_on = False

BLACK = (0, 0, 0)
BG_COLOR = (15, 15, 15)

game_folder = os.path.dirname(__file__)

FPS = 10
clock = pg.time.Clock()
ico = pg.image.load(game_folder+'./images/ico.png')
WIDTH = 800
HEIGHT = 600



pg.init()
video_infos = pg.display.Info()
width, height = video_infos.current_w, video_infos.current_h

screen = pg.display.set_mode((width-50, height-50),HWSURFACE|DOUBLEBUF|RESIZABLE)


bg = pg.image.load(game_folder+'./images/bg1.png')


pg.display.set_icon(ico)
pg.display.set_caption('Pillow FUN v1')
running = True

cur_f = 1

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        
        self.image = pg.image.load(game_folder+f'./images/c1_f{cur_f}.png')
        
        self.rect = self.image.get_rect()
        w, h = pg.display.get_surface().get_size()
        self.rect.center = (w/2+70, h/2+150)

    def update(self):
        cur_f = 1
        while cur_f<=3:
            cur_f +=1
            self.image = pg.image.load(game_folder+f'./images/c1_f{cur_f}.png')
            self.rect = self.image.get_rect()
            w, h = pg.display.get_surface().get_size()
            self.rect.center = (w/2+70, h/2+150)
            sleep(0.1)

        
        

        
        
all_sprites = pg.sprite.Group()
player = Player()
all_sprites.add(player)


while running:
    clock.tick(FPS)
    

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key==pg.K_LEFT:
                player.update()
                #all_sprites.update()
    if (serial_on):
        pillow_event = str(ser.readln())

    else:
        pillow_event = "No COM Device"
    
    #print (pillow_event)
    w, h = pg.display.get_surface().get_size()
    bg = pg.transform.scale(bg, (w, h))
    screen.blit(bg,(0,0))
    all_sprites.update()
    all_sprites.draw(screen)
    
    pg.display.flip()
    
    
pg.quit()
