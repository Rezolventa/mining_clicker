import pygame

from action import ActionManager, TimeManager
from consts import SCREEN_HEIGHT, SCREEN_WIDTH, TICKS_PER_SECOND
from display.cursor import my_set_cursor, MINING_CIRCLE_CURSOR, ARROW_CURSOR
from display.manager import DisplayManager
from game_state import GameState

pygame.init()


class MainController:
    def __init__(self):
        self.main_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.game_state = GameState()
        self.display_manager = DisplayManager(self.game_state, self.main_surface)
        self.action_manager = ActionManager(self.game_state, self.display_manager)
        self.time_manager = TimeManager()


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

        """    
        Для MVP выход из рейда и время не делаем
        # часы
        if main_controller.time_manager.tick == 0:
            hour = main_controller.time_manager.hour
            day = main_controller.time_manager.day
            main_controller.display_manager.clock.update_text(day, hour)
        """

        main_controller.time_manager.handle_routine()
        main_controller.action_manager.handle_routine()
        main_controller.display_manager.render_all()
        pygame.display.flip()


if __name__ == "__main__":
    main()
