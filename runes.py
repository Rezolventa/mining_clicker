import math
import random

from consts import RUNE_IMAGE_URLS, RUNE_MAX_SCORE, RUNE_TRIANGLE_RADIUS
from display.helpers import get_scaled_image


class Rune:
    def __init__(self, center_coords, image_url):
        self.image = get_scaled_image(image_url, 2)
        self.rect = self.image.get_rect()
        self.rect.center = (round(center_coords[0]), round(center_coords[1]))
        self.active = True
        self.frame_score = None

    def collidepoint(self, coords):
        return self.active and self.rect.collidepoint(coords)

    def click(self, frame_score):
        if not self.active:
            return False

        self.active = False
        self.frame_score = frame_score
        return True

    def draw(self, surface):
        if not self.active:
            return

        surface.blit(self.image, self.rect)


class RuneChallenge:
    rune_angles = (-math.pi / 2, math.pi / 6, 5 * math.pi / 6)

    def __init__(self, center_coords, radius=RUNE_TRIANGLE_RADIUS, max_score=RUNE_MAX_SCORE):
        self.frames_passed = 0
        self.max_score = max_score
        rune_images = RUNE_IMAGE_URLS.copy()
        random.shuffle(rune_images)
        rune_centers = [self.get_rune_center(center_coords, radius, angle) for angle in self.rune_angles]
        self.runes = [Rune(center, image_url) for center, image_url in zip(rune_centers, rune_images)]

    @staticmethod
    def get_rune_center(center_coords, radius, angle):
        return (
            center_coords[0] + radius * math.cos(angle),
            center_coords[1] + radius * math.sin(angle),
        )

    def add_frame(self):
        if not self.is_completed:
            self.frames_passed += 1

    def handle_click(self, coords):
        for rune in self.runes:
            if rune.collidepoint(coords):
                return rune.click(self.frames_passed)

        return False

    def draw(self, surface):
        for rune in self.runes:
            rune.draw(surface)

    @property
    def is_completed(self):
        return all(not rune.active for rune in self.runes)

    @property
    def score(self):
        total_frame_score = sum(rune.frame_score or 0 for rune in self.runes)
        return max(0, self.max_score - total_frame_score)
