from fileHandler import FileHandler
import pygame
from vectors import Vct

class MouseHandler:
    def __init__(self):
        self.clicked = False
        self.grab_node = None
        self.grab_start = Vct(0, 0)
        self.grab_offset = Vct(0, 0)
        self.offset = Vct(0, 0)
        self.last_mouse = Vct(0, 0)
        self.fh = FileHandler()

    def update(self, m1, ctrl, mouse_pos, master_node):
        mouse_node = self.on_node(mouse_pos-self.offset, master_node)
        master_node.unvisit()

        if m1:
            if not self.clicked:
                self.clicked = True
                self.grab_start = mouse_pos

                #master_node.apply_to_childs(lambda x: setattr(x, "draw_thumbnail", False, ignore_parent = True)
                #master_node.unvisit()

                if ctrl:
                    parent = mouse_node if mouse_node else master_node
                    new_node = to.create_child(parent)

                    self.switch_grabbed(new_node, master_node)
                    self.grab_offset = Vct(0, 0)
                else:
                    if mouse_node is not None:
                        self.switch_grabbed(mouse_node, master_node)
                        self.grap_offset = mouse_node.pos - mouse_pos + self.offset
            else:
                if self.grab_node is None:
                    self.offset += mouse_pos - self.last_mouse
                else:
                    self.grab_node.apply_to_childs(lambda x: x.move((x.pos - self.grab_node.pos) + mouse_pos - self.offset + self.grab_offset))

        else:
            self.grab_node = None
            self.clicked = False

            if mouse_node:
                if not mouse_node.draw_thumbnail:
                    mouse_node.need_reload = True
                mouse_node.draw_thumbnail = True
            else:
                pass
                #master_node.apply_to_childs(lambda x: setattr(x, "draw_thumbnail", False, ignore_parent = True)
                #master_node.unvisit()


        master_node.unvisit()
        self.last_mouse = mouse_pos

    def on_node(self, mouse_pos, node):
        if (mouse_pos - node.pos).mag() < node.radius:
            return node

        for n in node.childs:
            if on_children := self.on_node(mouse_pos, n):
                return on_children

        return None

    def switch_grabbed(self, switch_to, master_node):
        self.grab_node = switch_to

        # find selected node cuz its name may need change
        if self.fh.opened_file is not None: 
            selected_node = master_node.find_selected() 
            master_node.unvisit()
            new_name = self.fh.get_current_topic()
            selected_node.name = new_name
            selected_node.selected = False

        switch_to.selected = True

        self.fh.changed_to_file(switch_to.name)
