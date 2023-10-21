import os
import config
import pygame
from vectors import Vct
from fileHandler import get_correct_name, create_file

class Node:
    def __init__(self, pos, r, name):
        self.pos = pos
        self.des_pos = pos
        self.radius = r
        self.visited = False
        self.selected = False
        self.name = name
        self.childs = []
        self.draw_thumbnail = False
        self.thumbnail = None

    def draw(self, screen, mid, scaler, font):
        drawPos = (self.pos+mid)*scaler

        # draw the node itself
        pygame.draw.circle(screen, config.nodeColor, drawPos.int_tuple(), self.radius*scaler, config.line_width)

        # draw inner circle if selected
        if self.selected:
            pygame.draw.circle(screen, config.selected, drawPos.int_tuple(), (self.radius - 1)*scaler, config.line_width)

        # draw name of the node
        text_surface = font.render(self.name, True, (255, 255, 255))
        text_surface = pygame.transform.scale_by(text_surface, scaler)
        text_rect = text_surface.get_rect()
        text_rect.center = (drawPos + (Vct(0, self.radius + 10))*scaler).int_tuple()
        screen.blit(text_surface, text_rect)

        # draw lines to childrens
        for n in self.childs:
            pygame.draw.aaline(screen, config.arrows, drawPos.int_tuple(), ((n.pos+mid)*scaler).int_tuple(), config.line_width)

        # if mouse is on this node, draw thumbnail
        if self.draw_thumbnail:
            if self.thumbnail is None:
                self.reload_thumbnail()
            else:
                screen.blit(self.thumbnail, (mid + self.get_thubmnail_rect().topleft).int_tuple())

    def get_thubmnail_rect(self):
        rect = self.thumbnail.get_rect()
        rect.center = (self.pos - Vct(self.radius+10+rect.width//2, 0)).int_tuple()
        return rect

    def move(self, to):
        if self.draw_thumbnail:
            return
        self.des_pos = to

    def update(self):
        if self.pos == self.des_pos:
            return
        dif = self.des_pos - self.pos 
        if dif.mag() < 1:
            self.pos = self.des_pos
            return
        self.pos = self.pos + dif*0.1

    def apply_to_childs(self, foo, ignore_parent=False):
        self.visited = True

        if not ignore_parent:
            foo(self)

        for n in self.childs:
            if n.visited:
                continue
            n.apply_to_childs(foo)

    def unvisit(self):
        self.visited = False
        for n in self.childs:
            n.unvisit()

    def create_child(self, tpos):
        new_name = self.name + "subtopic"
        new_name = get_correct_name(new_name) 
        create_file(new_name)
        
        rad = config.defaultRadius if self.name == "master" else self.radius * config.child_scaler
        c = Node(tpos, rad, new_name)
        self.childs.append(c)
        return c

    def find_selected(self):
        if self.selected:
            return self

        for n in self.childs:
            if selected := n.find_selected():
                return selected

        return None
         

    def str(self):
        s = ""
        s += f"{self.name} --> (self.pos); childs={len(self.childs)}"
        for c in self.childs:
            s += "\n"
            s += "\t" + c.str() 

        return s

    def reload_thumbnail(self):
        try:
            self.thumbnail = pygame.image.load(f"{config.cache_dir}{self.name}-1.png")
        except (FileNotFoundError, pygame.error):
            print(f"trying to load {config.cache_dir}{self.name}-1.png, but the file was not genereted yet")
            return 

        
        # scale
        self.thumbnail = pygame.transform.smoothscale(self.thumbnail, config.thumbnail_size)

        # crop
        size = self.thumbnail.get_size()
        new_surface = pygame.Surface((size[0]-config.thumbnail_crop_by, size[1]-config.thumbnail_crop_by*1.41421))
        new_surface.blit(self.thumbnail, (-config.thumbnail_crop_by/2,-config.thumbnail_crop_by/2))
        self.thumbnail = new_surface
