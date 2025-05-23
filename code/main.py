import pygame
from vectors import Vct
import config
import initializer
from mouseHandler import MouseHandler, MouseInfo
from uiAligner import UIAligner

WHITE = (255, 255, 255)


def main():
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    end = False
    font = pygame.font.Font("src/JetBrains.ttf", config.fontSize)

    master_node = initializer.getMasterNode()
    master_node.apply_to_childs(lambda x: x.reload_thumbnail(), ignore_parent=True)

    mh = MouseHandler()
    mouse = MouseInfo()
    aligner = UIAligner()

    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
                pygame.quit()
                initializer.on_exit(master_node)
                exit()

            elif event.type == pygame.MOUSEWHEEL:
                mouse.scale(event.y * config.wheel_dist)

        keys = pygame.key.get_pressed()
        screen_size = Vct(pygame.display.Info().current_w, pygame.display.Info().current_h)
        mid = screen_size * 0.5
        mouse.update((Vct.fromTuple(pygame.mouse.get_pos()) * (1 / mouse.scaler)) - mid, pygame.mouse.get_pressed()[0], keys[pygame.K_LCTRL])

        mh.update(mouse, master_node, mid)
        screen.fill(config.background)

        master_node.apply_to_childs(lambda x: x.draw(screen, mid + mh.offset, mouse.scaler, font), ignore_parent=True)
        master_node.apply_to_childs(lambda x: x.update(), ignore_parent=True)
        master_node.apply_to_childs(lambda x: aligner.dump(x), ignore_parent=True)

        aligner.align()

        clock.tick(60)
        pygame.display.update()


if __name__ == "__main__":
    main()
