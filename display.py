import pygame

from conts import WHITE, SCREEN_WIDTH, SCREEN_HEIGHT, TICKS_PER_SECOND
from items import PoorIronOre, IronOre

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
    """
    Абстрактный класс для определения общих методов и их сигнатур
    """

    def add_animation_count(self):
        raise NotImplementedError

    def draw(self, surface):
        raise NotImplementedError


class DisplayManager:
    MINING_PAGE = "mining"
    CRAFTING_PAGE = "crafting"
    VENDOR_PAGE = "vendor"

    def __init__(self):
        self.main_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.buttons = self.init_panel_buttons()

        self.middle_screen = MiddleScreen()

        self.highlight_text_objects = []
        self.bank_table = BankTable((1000, 400))

        self.page = self.MINING_PAGE

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

        buttons = [mining_button, crafting_button, vendor_button]
        return buttons

    def render_all(self):
        self.main_surface.fill((0, 0, 0))

        for obj in self.buttons:
            obj.draw(self.main_surface)

        if self.page == self.MINING_PAGE:
            self.middle_screen.draw(self.main_surface)

            # если использовать self.highlight_text_objects, возникает баг отображения при удалении элемента "на лету"
            temp_list = self.highlight_text_objects.copy()
            for obj in temp_list:
                if obj.show:
                    obj.draw(self.main_surface)
                else:
                    self.highlight_text_objects.remove(obj)

        self.bank_table.draw(self.main_surface)

    def highlight_text(self, item_name, coords):
        self.highlight_text_objects.append(LiftingText(f"+1 {item_name}", coords))

    def get_animated_objects(self) -> list[AnimatedObject]:
        result = [self.middle_screen] + self.highlight_text_objects
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


class MiddleScreen(AnimatedObject):
    def __init__(self):
        self.background_image = get_scaled_image("sprites/middle_screen.png", 4)
        self.rect = self.background_image.get_rect()
        self.rect.topleft = (236, 0)

        self.ore_image = get_scaled_image("sprites/ore.png", 16)
        self.pickaxe_idle_image = get_scaled_image("sprites/pickaxe.png", 12)
        self.pickaxe_hit_image = get_scaled_image("sprites/pickaxe_hit.png", 12)

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


class ObjectRowIconAndText:
    def __init__(self, item, bottom_left_coords):
        self.item = item
        self.icon = get_scaled_image(item.image_url)
        self.icon_rect = self.icon.get_rect()
        self.icon_rect.bottomleft = bottom_left_coords

        self.quantity = 0

        self.text_image = default_font.render("x0", True, WHITE)
        self.text_rect = self.text_image.get_rect()
        self.text_rect.bottomleft = (self.icon_rect.bottomleft[0] + 30, self.icon_rect.bottomleft[1])

    def draw(self, surface):
        surface.blit(self.icon, self.icon_rect)
        surface.blit(self.text_image, self.text_rect)

    def add_quantity(self, quantity):
        self.quantity += quantity
        text_rect = self.text_rect
        self.text_image = default_font.render("x" + str(self.quantity), True, WHITE)
        self.text_rect = text_rect

    def __repr__(self):
        return self.item.slug


class BankTable:
    space_between_rows_px = 30

    def __init__(self, top_left_coords):
        self.top_left_coords = top_left_coords
        self.items_list = [PoorIronOre, IronOre]
        self.rows = []

        for item in self.items_list:
            self.top_left_coords = (self.top_left_coords[0], self.top_left_coords[1] + self.space_between_rows_px)
            self.rows.append(ObjectRowIconAndText(item, self.top_left_coords))

    def draw(self, surface):
        for row in self.rows:
            row.draw(surface)

    def get_row(self, item_slug: str) -> ObjectRowIconAndText:
        for row in self.rows:
            if row.item.slug == item_slug:
                return row
