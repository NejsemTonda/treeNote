import os
import config
import pygame

class Node:
    def __init__(self, pos, r, name):
        self.pos = pos
        #self.des_pos = pos
        self.radius = r
        self.visited = False
        self.selected = False
        self.name = name
        self.childs = []
        #self.need_reload = True
        self.draw_thumbnail = False
        #self.thumbnail = None

    def draw(self, screen, mid, font):
        if self.name == "master":
            return

        drawPos = self.pos+mid 


        pygame.draw.circle(screen, config.nodeColor, drawPos.tuple(), self.radius, config.line_width)
        print(f"drawing {self.name}")

        if self.selected:
            pygame.draw.circle(screen, config.selected, drawPos.tuple(), self.radius - 1, config.line_width)

        #text_surface = font.render(self.name, True, (255, 255, 255))
        #text_rect = text_surface.get_rect(center=(act_pos[0], act_pos[1] + int(self.radius) + 10))
        #screen.blit(text_surface, text_rect)

        for n in self.childs:
            pygame.draw.aaline(screen, config.arrows, drawPos.tuple(), (n.pos+mid).tuple(), config.line_width)

        #if self.draw_thumbnail and self.thumbnail:
        #    thumbnail_rect = self.get_thumbnail_rect()
        #    thumbnail_rect = pygame.Rect(thumbnail_rect[0] + int(mid[0]), thumbnail_rect[1] + int(mid[1]), thumbnail_rect[2], thumbnail_rect[3])
        #    screen.blit(self.thumbnail, thumbnail_rect)

    #def get_thumbnail_rect(self):
    #    return (int(self.pos[0]) - config.thumbnail_size_x - int(self.radius * 1.5), int(self.pos[1]) - config.thumbnail_size_y // 2, config.thumbnail_size_x, config.thumbnail_size_y)

    def move(self, to):
        self.des_pos = to

    def update(self):
        if self.draw_thumbnail:
            return
        if self.pos == self.des_pos:
            return
        dif = pygame.math.Vector2(self.des_pos[0] - self.pos[0], self.des_pos[1] - self.pos[1])
        if dif.length() < 1:
            self.pos = self.des_pos
            return
        self.pos = (self.pos[0] + dif[0] / 10, self.pos[1] + dif[1] / 10)

    def apply_to_childs(self, foo):
        self.visited = True
        for n in self.childs:
            if n.visited:
                continue
            n.apply_to_childs_and_parent(foo)

    def apply_to_childs_and_parent(self, foo):
        self.visited = True
        foo(self)
        self.apply_to_childs(foo)

    def unvisit(self):
        self.visited = False
        for n in self.childs:
            n.unvisit()

    def create_child(self, tpos):
        new_name = self.name + "subtopic"
        if os.path.exists(config.notes_dir + new_name + config.ext):
            x = 1
            while os.path.exists(config.notes_dir + new_name + str(x) + config.ext):
                x += 1
            new_name = self.name + "subtopic" + str(x)

        rad = config.default_node_size if self.name == "master" else self.radius * config.child_scaler
        c = Node(tpos, rad, new_name)
        self.childs.append(c)
        return c

    def str(self):
        s = ""
        s += f"{self.name} --> (self.pos); childs={len(self.childs)}"
        for c in self.childs:
            s += "\n"
            s += "\t" + c.str() 

        return s
"""
    def reload_thumbnail(self):
        if not self.need_reload:
            return
        self.need_reload = False
        try:
            print(f"Reloading thumbnail for {self.name}")
            raw_png = pygame.image.load(config.cache_dir + self.name + "-thumbnail-1.png")

            new_bounds = raw_png.get_rect()
            resize_by = config.crop_thumbnail
            new_bounds.x += resize_by
            new_bounds.y += resize_by
            new_bounds.width -= resize_by * 2
            new_bounds.height -= resize_by * 2

            cropped_surface = pygame.Surface((new_bounds.width, new_bounds.height), pygame.SRCALPHA)

            for x in range(new_bounds.width):
                for y in range(new_bounds.height):
                    cropped_surface.set_at((x, y), raw_png.get_at((x + new_bounds.x, y + new_bounds.y)))

            self.thumbnail = pygame.transform.smoothscale(cropped_surface, (config.thumbnail_size_x, config.thumbnail_size_y))
        except FileNotFoundError:
            print(config.cache_dir + self.name + "-thumbnail-1.png" + " was not generated")
        except pygame.error:
            print(config.cache_dir + self.name + "-thumbnail-1.png" + " the image format is not supported or was not generated properly")
        except FileNotFoundError:
            Game1.print_no_init()
"""
