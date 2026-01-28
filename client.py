import pygame

from action import ActionManager
from display.consts import TICKS_PER_SECOND
from display.cursor import my_set_cursor, MINING_CIRCLE_CURSOR, ARROW_CURSOR
from display.manager import DisplayManager

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

        # курсор
        hovered_object = main_controller.action_manager.get_hovered_object()
        if hovered_object == main_controller.action_manager.display_manager.middle_screen_background_image:
            my_set_cursor(MINING_CIRCLE_CURSOR)
        else:
            my_set_cursor(ARROW_CURSOR)


        main_controller.action_manager.handle_routine()
        main_controller.display_manager.render_all()
        pygame.display.flip()


if __name__ == '__main__':
    main()