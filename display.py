import pygame


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

WHITE = (255, 255, 255)


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


class DisplayManager:
    def __init__(self):
        self.main_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.buttons = self.init_panel_buttons()

        # main_screen - refactoring as Sprite
        self.main_screen = get_scaled_image("sprites/main_screen.png", 4)
        main_screen_rect = self.main_screen.get_rect()
        main_screen_rect.topleft = (236, 0)

        self.ore_sprite = get_scaled_image("sprites/ore.png", 12)

        self.pickaxe_sprite = get_scaled_image("sprites/pickaxe.png", 8)

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

        # main_screen
        self.main_surface.blit(self.main_screen, (236, 0))
        self.main_surface.blit(self.ore_sprite, (400, 250))
        self.main_surface.blit(self.pickaxe_sprite, (500, 250))



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


# class Screen(pygame.sprite.Sprite):
#     def __init__(self):
#         pass

