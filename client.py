import pygame

from action import ActionManager
from conts import TICKS_PER_SECOND
from display import DisplayManager

pygame.init()


class MainController:
    def __init__(self):
        self.display_manager = DisplayManager()
        self.action_manager = ActionManager(self)


def main():
    main_controller = MainController()
    clock = pygame.time.Clock()

    running = True

    while running:
        clock.tick(TICKS_PER_SECOND)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONUP:
                main_controller.action_manager.handle_mouse_click()

        main_controller.action_manager.handle_routine()
        main_controller.display_manager.render_all()
        pygame.display.flip()


if __name__ == '__main__':
    main()