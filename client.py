import pygame

from action import ActionManager
from display import DisplayManager

pygame.init()
pygame.font.init()


class MainController:
    def __init__(self):
        self.display_manager = DisplayManager()
        self.action_manager = ActionManager(self)


def main():
    main_controller = MainController()
    clock = pygame.time.Clock()

    running = True

    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                break
            elif event.type == pygame.MOUSEBUTTONUP:
                main_controller.action_manager.handle_mouse_click()

        if running:
            main_controller.action_manager.handle_routine()
            main_controller.display_manager.render_all()
            pygame.display.flip()

if __name__ == '__main__':
    main()