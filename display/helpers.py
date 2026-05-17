import pygame

from consts import WHITE


def get_scaled_image(image, k=1) -> pygame.surface.Surface:
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


class StopDrawSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


stop_draw = StopDrawSingleton()


class AnimatedObjectV2:
    """
    Абстрактный класс для определения общих методов и их сигнатур.
    """

    frame_image = None
    animation_count = None
    image = None
    rect = None

    def add_animation_count(self):
        if image := self.frame_image.get(self.animation_count):
            self.image = image
        self.animation_count += 1

    def draw(self, surface):
        if self.image is stop_draw:
            return

        surface.blit(self.image, self.rect)


class EndRunScreen(AnimatedObjectV2):
    def __init__(self):
        self.end_run_screen_1 = get_scaled_image("sprites/end_run_screen_1.png", 3)
        self.end_run_screen_2 = get_scaled_image("sprites/end_run_screen_2.png", 3)

        self.frame_image = {
            0: self.end_run_screen_1,
            10: self.end_run_screen_2,
            20: self.end_run_screen_1,
            30: self.end_run_screen_2,
            40: self.end_run_screen_1,
            50: stop_draw,
        }

        self.animation_count = 50

        rect = self.end_run_screen_1.get_rect()
        rect.topleft = (400, 200)
        self.rect = rect

        self.image = stop_draw

    def start(self):
        self.animation_count = 0
        self.image = self.end_run_screen_1


class CommonSprite:
    def __init__(self, image):
        self.image = image
        self.rect = image.get_rect()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


import math
import random


def get_random_point_in_circle(center_x, center_y, radius):
    angle = random.uniform(0, 2 * math.pi)
    distance = math.sqrt(random.uniform(0, 1)) * radius

    x = center_x + distance * math.cos(angle)
    y = center_y + distance * math.sin(angle)

    return x, y
