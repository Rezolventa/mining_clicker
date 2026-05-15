from consts import DEFAULT_FONT, TICKS_PER_SECOND, WHITE
from display.buttons import GoldenIngotButton, IronIngotButton, LavaIngotButton, PoorIronIngotButton, SilverIngotButton
from display.helpers import AnimatedObject, AnimatedObjectV2, get_scaled_image, stop_draw


class PickaxeHit(AnimatedObjectV2):
    def __init__(self):
        """
        Эталонный класс с анимацией и остановкой анимации
        """
        self.pickaxe_idle_image = get_scaled_image("sprites/pickaxe.png", 2)
        self.pickaxe_hit_image = get_scaled_image("sprites/pickaxe_hit.png", 2)

        self.animation_count = 0

        self.frame_image = {
            0: self.pickaxe_idle_image,
            4: self.pickaxe_hit_image,
            7: stop_draw,
        }

        self.rect = None
        self.image = self.pickaxe_idle_image
        self.set_coords((0, 0))
        self.image = stop_draw

    def start(self, coords):
        self.animation_count = 0
        self.image = self.pickaxe_idle_image
        self.set_coords(coords)

    def set_coords(self, coords):
        rect = self.image.get_rect()
        rect.bottomleft = coords
        self.rect = rect


# TODO: это то же самое, что CraftingPageManager?
class CraftingMiddleScreen(AnimatedObject):
    def __init__(self):
        self.crafting_poor_iron_ingot = PoorIronIngotButton()
        self.crafting_poor_iron_ingot.rect.topleft = (300, 250)

        self.crafting_iron_ingot = IronIngotButton()
        self.crafting_iron_ingot.rect.topleft = (450, 250)

        self.crafting_silver_ingot = SilverIngotButton()
        self.crafting_silver_ingot.rect.topleft = (600, 250)

        self.crafting_golden_ingot = GoldenIngotButton()
        self.crafting_golden_ingot.rect.topleft = (300, 400)

        self.crafting_lava_ingot = LavaIngotButton()
        self.crafting_lava_ingot.rect.topleft = (450, 400)

        self.group = [
            self.crafting_poor_iron_ingot,
            self.crafting_iron_ingot,
            self.crafting_silver_ingot,
            self.crafting_golden_ingot,
            self.crafting_lava_ingot,
        ]

    def draw(self, surface):
        for sprite in self.group:
            sprite.draw(surface)


class LiftingText(AnimatedObject):
    animation_speed = 3
    time_to_live_seconds = 2

    def __init__(self, text, coords: tuple):
        self.text = text
        self.image = DEFAULT_FONT.render(text, True, WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = coords
        self.show = True

        self.animation_count = 0

    def draw(self, surface):
        # TODO: переместить в add_animation_count
        x = self.rect.topleft[0]
        y = self.rect.topleft[1]
        self.rect.topleft = (x, y - 1)

        surface.blit(self.image, self.rect)

    def add_animation_count(self):
        ticks_to_live = self.time_to_live_seconds * TICKS_PER_SECOND
        self.animation_count += 1
        if self.animation_count == ticks_to_live:
            self.animation_count = 0
            self.show = False
