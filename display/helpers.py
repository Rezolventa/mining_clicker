import pygame

from display.consts import WHITE


def get_scaled_image(image, k = 1) -> pygame.surface.Surface:
    """
    Подгружает спрайт и увеличивает его размер в k раз.
    """
    image = pygame.image.load(image)

    if image.get_alpha():
        image = image.convert_alpha()
    else:
        image = image.convert()
        image.set_colorkey(WHITE)

    size = image.get_size()
    return pygame.transform.scale(image, (int(size[0] * k), int(size[1] * k)))


class AnimatedObject:
    """
    Абстрактный класс для определения общих методов и их сигнатур.
    Используется для типизации и проверки типов.
    """

    def add_animation_count(self):
        raise NotImplementedError

    def draw(self, surface):
        raise NotImplementedError


class CommonSprite:
    def __init__(self, image):
        self.image = image
        self.rect = image.get_rect()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


import random
import math

def get_random_point_in_circle(center_x, center_y, radius):
    angle = random.uniform(0, 2 * math.pi)
    distance = math.sqrt(random.uniform(0, 1)) * radius

    x = center_x + distance * math.cos(angle)
    y = center_y + distance * math.sin(angle)

    return x, y