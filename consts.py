import pygame

TICKS_PER_SECOND = 30
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
ENABLE_HIT_CIRCLES = False
ENABLE_RUNES = True
RUNE_APPEAR_CHANCE = 0.25
RUNE_TRIANGLE_RADIUS = 45
RUNE_MAX_SCORE = 300
RUNE_IMAGE_URLS = [
    "sprites/shovel_rune.png",
    "sprites/pickaxe_rune.png",
    "sprites/sledgehammer_rune.png",
]

WHITE = (255, 255, 255)

pygame.font.init()
DEFAULT_FONT = pygame.font.SysFont("serif", 30)
