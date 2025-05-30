from fileHandler import FileHandler, check_for_delete
from vectors import Vct
import config


class MouseHandler:
    def __init__(self):
        self.clicked = False
        self.grab_node = None
        self.grab_start = Vct(0, 0)
        self.grab_offset = Vct(0, 0)
        self.offset = Vct(0, 0)
        self.last_mouse = Vct(0, 0)
        self.last_scale = 1
        self.fh = FileHandler()
        self.thumbnail_timer = 0
        self.grap_offset = None

    def update(self, mouse, master_node, mid):
        mouse_node = self.on_node(mouse.pos - self.offset, master_node)

        self.offset += (1 - mouse.scaler / self.last_scale) * (mouse.pos + mid)

        if mouse.m1:
            if not self.clicked:
                self.clicked = True
                self.grab_start = mouse.pos

                master_node.apply_to_childs(lambda x: setattr(x, "draw_thumbnail", False), ignore_parent=True)

                if mouse.ctrl:
                    parent = mouse_node if mouse_node else master_node
                    new_node = parent.create_child(mouse.pos - self.offset)

                    self.switch_grabbed(new_node, master_node)
                    self.grab_offset = Vct(0, 0)
                else:
                    if mouse_node is not None:
                        mouse_node.reload_thumbnail()
                        self.switch_grabbed(mouse_node, master_node)
                        self.grap_offset = mouse_node.pos - mouse.pos + self.offset
            else:
                if self.grab_node is None:
                    self.offset += mouse.pos - self.last_mouse
                else:
                    # self.grab_node.apply_to_childs(lambda x: x.move((x.pos - self.grab_node.pos) + mouse.pos - self.offset))
                    self.grab_node.apply_to_childs(lambda x: x.shift(mouse.pos - self.last_mouse))

        else:
            self.grab_node = None
            self.clicked = False

            if mouse_node:
                self.thumbnail_timer += 1
                if self.thumbnail_timer > config.thumbnail_wait_time:
                    mouse_node.draw_thumbnail = True
            else:
                master_node.apply_to_childs(lambda x: setattr(x, "draw_thumbnail", False), ignore_parent=True)
                self.thumbnail_timer = 0

        master_node.apply_to_childs(lambda x: check_for_delete(x))

        self.last_mouse = mouse.pos
        self.last_scale = mouse.scaler

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
            new_name = self.fh.get_current_topic()
            selected_node.name = new_name
            selected_node.selected = False

        switch_to.selected = True

        self.fh.changed_to_file(switch_to.name)


class MouseInfo:
    def __init__(self):
        self.pos = Vct(0, 0)
        self.ctrl = False
        self.m1 = False
        self.scaler = 1

    def update(self, pos, m1, ctrl):
        self.pos = pos
        self.ctrl = ctrl
        self.m1 = m1

    def scale(self, scaler):
        new_scale = self.scaler + scaler
        self.scaler = new_scale
