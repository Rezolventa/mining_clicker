import pygame


class Cursor:
    cursor_surface = None

    def set_cursor(self):
        pass


class ArrowCursor(Cursor):
    cursor_surface = pygame.cursors.arrow

    def __init__(self):
        pass

    def set_cursor(self):
        cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
        pygame.mouse.set_cursor(cursor)


class MiningCircleCursor(Cursor):
    cursor_surface = pygame.image.load("sprites/crosshair.png")
    hotspot = (16, 16)

    def __init__(self):
        pass

    def set_cursor(self):
        cursor = pygame.cursors.Cursor(self.hotspot, self.cursor_surface)
        pygame.mouse.set_cursor(cursor)


ARROW_CURSOR = "arrow_cursor"
MINING_CIRCLE_CURSOR = "mining_circle"

CURSOR_MAP = {
    ARROW_CURSOR: ArrowCursor(),
    MINING_CIRCLE_CURSOR: MiningCircleCursor(),
}


def my_set_cursor(cursor: str) -> None:
    CURSOR_MAP[cursor].set_cursor()
