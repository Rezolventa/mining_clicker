import pygame
from pygame import Surface

from display.bank import BankTable
from display.consts import WHITE, SCREEN_WIDTH, SCREEN_HEIGHT, TICKS_PER_SECOND, DEFAULT_FONT
from display.helpers import get_scaled_image, AnimatedObject, CommonSprite


class DisplayManager:
    MINING_PAGE = "mining"
    CRAFTING_PAGE = "crafting"
    VENDOR_PAGE = "vendor"

    def __init__(self):
        self.main_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.page = self.MINING_PAGE

        # TODO: этот CommonSprite на хрен не нужен, лучше в draw напрямую указывать координаты, т.к. это статика
        self.middle_screen_background_image = CommonSprite(get_scaled_image("sprites/middle_screen.png", 4))
        self.middle_screen_background_image.rect.topleft = (236, 0)

        # главная панель
        self.buttons = self.init_panel_buttons()

        # основной экран
        # mining
        self.mining_middle_screen = MiningMiddleScreen()
        self.pickaxe = PickaxeHit()
        self.highlight_text_objects = []
        self.pickaxe_hit_circles = []

        # crafting
        self.crafting_middle_screen = CraftingMiddleScreen()

        # банк/инвентарь
        self.bank_table = BankTable((1000, 400))

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
            "vendor_button",
            get_scaled_image("sprites/vendor_button_on.png", 2),
            get_scaled_image("sprites/vendor_button_off.png", 2),
        )
        vendor_button.rect.bottomleft = (0, SCREEN_HEIGHT)

        buttons = [mining_button, crafting_button, vendor_button]
        return buttons

    def render_common_ui(self):
        for obj in self.buttons:
            obj.draw(self.main_surface)

        self.middle_screen_background_image.draw(self.main_surface)

    def render_all(self):
        self.main_surface.fill((0, 0, 0))

        if self.page == self.MINING_PAGE:
            self.mining_middle_screen.draw(self.main_surface)
            self.pickaxe.draw(self.main_surface)

            # если использовать self.highlight_text_objects, возникает баг отображения при удалении элемента "на лету"
            temp_list = self.highlight_text_objects.copy()
            for obj in temp_list:
                if obj.show:
                    obj.draw(self.main_surface)
                else:
                    self.highlight_text_objects.remove(obj)

            for hit_circle in self.pickaxe_hit_circles:
                hit_circle.draw(self.main_surface)
        elif self.page == self.CRAFTING_PAGE:
            self.crafting_middle_screen.draw(self.main_surface)

        self.render_common_ui()

        self.bank_table.draw(self.main_surface)

    def highlight_text(self, item_name, coords):
        self.highlight_text_objects.append(LiftingText(f"+1 {item_name}", coords))

    def get_animated_objects(self) -> list[AnimatedObject]:
        result = [self.pickaxe] + self.highlight_text_objects
        return result

    def add_animation_count(self):
        # TODO: каждый раз вычислять get_animated_objects это неоптимально
        for obj in self.get_animated_objects():
            obj.add_animation_count()

    def add_hit_circle(self, center_coords):
        """
        Мне не очень нравится этот метод, т.к. ему не место в этом классе
        """
        self.pickaxe_hit_circles.append(HitCircle(center_coords))


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        name: str,
        image_on,
        image_off,
        on: bool = False
    ):
        super().__init__()
        self.name = name
        self.image_on = image_on
        self.image_off = image_off

        self.on = on

        self.image = self.image_on if on else self.image_off
        self.rect = self.image.get_rect()

    def __repr__(self):
        return self.name

    def update(self):
        if self.on:
            self.image = self.image_on
        else:
            self.image = self.image_off

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class MiningMiddleScreen:
    def __init__(self):
        self.middle_screen_background_image = get_scaled_image("sprites/mining_background.png", 4)

    def draw(self, surface):
        surface.blit(self.middle_screen_background_image, (236, 0))


class StopDrawSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


stop_draw = StopDrawSingleton()


class PickaxeHit(AnimatedObject):
    def __init__(self):
        self.pickaxe_idle_image = get_scaled_image("sprites/pickaxe.png", 2)
        self.pickaxe_hit_image = get_scaled_image("sprites/pickaxe_hit.png", 2)

        self.animation_count = 0

        self.frame_image = {
            0: self.pickaxe_idle_image,
            12: self.pickaxe_hit_image,
            27: self.pickaxe_idle_image,
            39: stop_draw,
        }

        self.image = self.pickaxe_idle_image

    def add_animation_count(self):
        if image := self.frame_image.get(self.animation_count):
            self.image = image
        self.animation_count += 1

    def draw(self, surface):
        if self.image is stop_draw:
            return

        rect = self.image.get_rect()
        rect.bottomleft = pygame.mouse.get_pos()
        surface.blit(self.image, rect)

    def do_pickaxe_hit(self):
        self.animation_count = 0


class CraftingMiddleScreen(AnimatedObject):
    def __init__(self):
        self.crafting_recipe_image = CommonSprite(get_scaled_image("sprites/crafting_iron_ingot.png", 4))
        self.crafting_recipe_image.rect.topleft = (300, 250)

    def draw(self, surface):
        self.crafting_recipe_image.draw(surface)


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
