import pygame
from vectors import Vct
import config
import math

def draw_node(screen, node, pos, scaler):
    # draw the node itself
    pygame.draw.circle(screen, config.nodeColor, pos.int_tuple(), node.radius*scaler, config.line_width)

    # draw inner circle if selected
    if node.selected:
        pygame.draw.circle(screen, config.selected, pos.int_tuple(), (node.radius - 1)*scaler, config.line_width)

def draw_name(screen, node, pos, scaler, font):
    text_surface = font.render(node.name, True, (255, 255, 255))
    text_surface = pygame.transform.scale_by(text_surface, scaler)
    text_rect = text_surface.get_rect()
    text_rect.center = (pos + (Vct(0, node.radius + 10))*scaler).int_tuple()
    screen.blit(text_surface, text_rect)

def draw_connections(screen, node, pos, scaler):
    mid = (pos*(1/scaler) - node.pos)
    for n in node.childs:
        diff = (n.pos - node.pos).norm()
        draw_arrow(screen, pos+(diff*node.radius*scaler), (n.pos+mid-diff*n.radius)*scaler)

def draw_thumbnail(screen, node, pos, scaler):
    if node.thumbnail is None:
        node.reload_thumbnail()
    else:
       screen.blit(node.thumbnail, (pos - node.pos + node.get_thubmnail_rect().topleft).int_tuple())

def draw_arrow(screen, start, end):
    arrow_size = 10
    angle = -math.atan2(*(end-start).int_tuple())+math.pi/2
    

    # Draw the arrowhead
    arrow_leg1 = (end[0] - arrow_size * math.cos(angle - math.pi / 6),
                  end[1] - arrow_size * math.sin(angle - math.pi / 6))

    arrow_leg2 = (end[0] - arrow_size * math.cos(angle + math.pi / 6),
                  end[1] - arrow_size * math.sin(angle + math.pi / 6))

    pygame.draw.line(screen, config.arrows, start.int_tuple(), end.int_tuple(), 1)
    pygame.draw.line(screen, config.arrows, arrow_leg1, end.int_tuple(), 1)
    pygame.draw.line(screen, config.arrows, arrow_leg2, end.int_tuple(), 1)
