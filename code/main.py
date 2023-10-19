import os
import sys
import pygame
import numpy as np
import time
import math
from vectors import Vct
import config
import initializer
from mouseHandler import MouseHandler, MouseInfo

pygame.init()

WHITE = (255,255,255)
screen = pygame.display.set_mode((0,0), pygame.RESIZABLE)
clock = pygame.time.Clock()
end = False
font = pygame.font.Font('../src/font.ttf', config.fontSize)


master_node = initializer.getMasterNode()
mh = MouseHandler()
mouse = MouseInfo()

while not end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            end = True
            pygame.quit()
            initializer.on_exit(master_node)
            exit()

        elif event.type == pygame.MOUSEWHEEL:
            mouse.scale(event.y*config.wheel_dist)
     
    keys = pygame.key.get_pressed()
    screenSize = Vct(pygame.display.Info().current_w, pygame.display.Info().current_h)
    mid = screenSize * 0.5
    mouse.update(pos = (Vct.fromTuple(pygame.mouse.get_pos())*(1/mouse.scaler)) - mid,
                 m1 = pygame.mouse.get_pressed()[0],
                 ctrl = keys[pygame.K_LCTRL])
 
    mh.update(mouse, master_node, mid)
    screen.fill((0,0,0))

    #pygame.draw.circle(screen, (255,0,0), ((mouse.pos+mid)*mouse.scaler).int_tuple(), 10)
    master_node.apply_to_childs(lambda x : x.draw(screen, mid+mh.offset, mouse.scaler, font), ignore_parent = True)
    master_node.unvisit()

    master_node.apply_to_childs(lambda x : x.update(), ignore_parent = True)
    master_node.unvisit()

    clock.tick(60)
    pygame.display.update()

    
    
