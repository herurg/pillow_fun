import pygame as pg
import os
from pygame.locals import *
import serial


#Open Art SDXL


serial_on = True
try:
    ser = serial.Serial("COM11", 115200)
except:
    serial_on = False

BLACK = (0, 0, 0)

game_folder = os.path.dirname(__file__)

FPS = 20
clock = pg.time.Clock()
ico = pg.image.load(game_folder+'./images/ico.png')
WIDTH = 800
HEIGHT = 600


screen = pg.display.set_mode((WIDTH, HEIGHT),HWSURFACE|DOUBLEBUF|RESIZABLE)
pg.display.set_icon(ico)
pg.display.set_caption('Pillow FUN v1')
running = True


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50,50))
        self.image.fill('GREEN')
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)

    def update(self):
        self.rect.x +=5
        if self.rect.left >WIDTH:
            self.rect.right = 0
        
        
all_sprites = pg.sprite.Group()
player = Player()
all_sprites.add(player)


while running:
    clock.tick(FPS)
    w, h = pg.display.get_surface().get_size()
    print(w," ",h)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    if (serial_on):
        pillow_event = str(ser.readln())

    else:
        pillow_event = "No COM Device"
    #print (pillow_event)

    all_sprites.update()
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    pg.display.flip()
    
    
pg.quit()
