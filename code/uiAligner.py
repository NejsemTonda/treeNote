import pygame
from vectors import Vct

class UIAligner:
    def __init__(self):
        self.node_pile = []
        self.remembered_positions = []
        self.nodes_outofplace = False

    def dump(self, n):
        if n not in self.node_pile:
            self.node_pile.append(n)

    def align(self):
        for n1 in self.node_pile:
            for n2 in self.node_pile:
                if n1 == n2:
                    continue

                diff = n2.pos - n1.pos 

                if diff.mag() < n1.radius + n2.radius:
                    overlap_size = n1.radius + n2.radius - diff.mag()
                    n1.move(n1.pos - diff*overlap_size)
                    n1.move(n2.pos - diff*overlap_size)

        mouse_node = next((n for n in self.node_pile if n.draw_thumbnail), None)

        if mouse_node is None and self.nodes_outofplace:
            for i, n in enumerate(self.node_pile):
                n.move(self.remembered_positions[i])

            self.nodes_outofplace = False

        if mouse_node is not None and not self.nodes_outofplace:
            self.nodes_outofplace = True
            thumbnail_rect = mouse_node.get_thubmnail_rect()

            self.remembered_positions = [n.des_pos for n in self.node_pile]

            for n in self.node_pile:
                if self.is_overlaping(thumbnail_rect, n):
                    n.move(n.pos+self.get_resolving_vct(thumbnail_rect, n))

    def is_overlaping(self, rect, n):
        closest_x = max(rect.x, min(n.pos.x, rect.x + rect.width))
        closest_y = max(rect.y, min(n.pos.y, rect.y + rect.height))
        closest = Vct(closest_x, closest_y)
        
        return (closest-n.pos).mag() <= n.radius

    def get_resolving_vct(self, rect, n):
        left = abs(rect.x - n.pos.x)
        right = abs(rect.x + rect.width - n.pos.x)
        up = abs(rect.y - n.pos.y)
        down = abs(rect.y + rect.height - n.pos.y)
        
        margin = n.radius*1.5 
        shortest = min(left, right, up, down)

        if left == shortest:
            return Vct(-(left+margin), 0)
        elif right == shortest:
            return Vct(right+margin, 0)
        elif up == shortest:
            return Vct(0, -(up+margin))
        elif down == shortest:
            return Vct(0, (down+margin))
