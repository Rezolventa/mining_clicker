import pygame

from conts import WHITE, SCREEN_WIDTH, SCREEN_HEIGHT, TICKS_PER_SECOND

pygame.font.init()
default_font = pygame.font.SysFont("serif", 30)


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
    def add_animation_count(self):
        raise NotImplementedError

    def draw(self, surface):
        raise NotImplementedError


class DisplayManager:
    def __init__(self):
        self.main_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.buttons = self.init_panel_buttons()

        self.main_screen = MainScreen()

        self.other_object = []

    def init_panel_buttons(self):
        mining_button = Button(
            "mining_button",
            get_scaled_image("sprites/mining_button_on.png", 2),
            get_scaled_image("sprites/mining_button_off.png", 2),
            True,
        )
        mining_button.rect.bottomleft = (0, SCREEN_HEIGHT - 240)

        crafting_button = Button(
            "crafting_button",
            get_scaled_image("sprites/crafting_button_on.png", 2),
            get_scaled_image("sprites/crafting_button_off.png", 2),
        )
        crafting_button.rect.bottomleft = (0, SCREEN_HEIGHT - 120)

        vendor_button = Button(
            "crafting_button",
            get_scaled_image("sprites/vendor_button_on.png", 2),
            get_scaled_image("sprites/vendor_button_off.png", 2),
        )
        vendor_button.rect.bottomleft = (0, SCREEN_HEIGHT)

        return [mining_button, crafting_button, vendor_button]

    def render_all(self):
        self.main_surface.fill((0, 0, 0))

        for obj in self.buttons:
            obj.draw(self.main_surface)

        self.main_screen.draw(self.main_surface)

        for obj in self.other_object:
            if obj.show:
                obj.draw(self.main_surface)
            else:
                self.other_object.remove(obj)

    def highlight_text(self, coords):
        self.other_object.append(LiftingText("test text", coords))

    def get_animated_objects(self) -> list[AnimatedObject]:
        result = [self.main_screen] + self.other_object
        return result

    def add_animation_count(self):
        for obj in self.get_animated_objects():
            obj.add_animation_count()


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        name: str,
        sprite_on,
        sprite_off,
        on: bool = False
    ):
        super().__init__()
        self.name = name
        self.sprite_on = sprite_on
        self.sprite_off = sprite_off

        self.on = on

        self.image = self.sprite_on if on else self.sprite_off
        self.rect = self.image.get_rect()

    def __repr__(self):
        return self.name

    def update(self):
        if self.on:
            self.image = self.sprite_on
        else:
            self.image = self.sprite_off

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class MainScreen(AnimatedObject):
    def __init__(self):
        self.background_image = get_scaled_image("sprites/main_screen.png", 4)
        self.rect = self.background_image.get_rect()
        self.rect.topleft = (236, 0)

        self.ore_image = get_scaled_image("sprites/ore.png", 12)
        self.pickaxe_idle_image = get_scaled_image("sprites/pickaxe.png", 8)
        self.pickaxe_hit_image = get_scaled_image("sprites/pickaxe_hit.png", 8)

        self.animation_count = 0
        self.animation_count_limit = 5

        self.pickaxe_hit = False
        self.pickaxe_image = self.pickaxe_idle_image

    def do_pickaxe_hit(self):
        self.pickaxe_hit = True
        self.animation_count = 0
        self.pickaxe_image = self.pickaxe_hit_image

    def add_animation_count(self):
        self.animation_count += 1
        if self.animation_count == self.animation_count_limit:
            self.animation_count = 0
            self.pickaxe_hit = False
            self.pickaxe_image = self.pickaxe_idle_image

    def draw(self, surface):
        surface.blit(self.background_image, self.rect)
        surface.blit(self.ore_image, (400, 250))
        surface.blit(self.pickaxe_image, (500, 250))


class LiftingText(AnimatedObject):
    animation_speed = 3
    time_to_live_seconds = 2

    def __init__(self, text, coords: tuple):
        self.text = text
        self.image = default_font.render(text, True, WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = coords
        self.show = True

        self.animation_count = 0

    def draw(self, surface):
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


# class StableText:
#     def __init__(self, text, coords: tuple):
#
#
# class RowImageAndText:
#     def __init__(self, image, initial_text):
#         self.image


