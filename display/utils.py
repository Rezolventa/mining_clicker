import pygame

from consts import DEFAULT_FONT, WHITE
from display.buttons import Button
from display.helpers import get_scaled_image


class HitCircle:
    def __init__(self, center_coords):
        self.image = get_scaled_image("sprites/hit_circle.png")
        self.rect = self.image.get_rect()
        self.rect.center = center_coords
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, surface):
        """
        Возможно придётся рисовать видимые кружки сверху, а невидимые за фоном,
        чтобы можно было проверять на коллизии
        """
        surface.blit(self.image, self.rect)


class Clock:
    def __init__(self, coords: tuple):
        self.image = DEFAULT_FONT.render("DAY: 0  ---  0:00", True, WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = coords
        self.show = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update_text(self, day, hour):
        text = f"DAY: {day}  ---  {hour}:00"
        self.image = DEFAULT_FONT.render(text, True, WHITE)


class SelectorUI:
    """
    Из всех элементов активен может быть только один.
    """

    def __init__(self, buttons: list[Button]):
        self.buttons = buttons
        self.active_button = None

    def set_active_button(self, new_active_button: Button) -> None:
        for button in self.buttons:
            if button == new_active_button:
                button.on = True
            else:
                button.on = False
            button.update()

        self.active_button = new_active_button
