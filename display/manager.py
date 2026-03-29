import pygame

from display.bank import Bank, Inventory
from consts import WHITE, SCREEN_WIDTH, SCREEN_HEIGHT, TICKS_PER_SECOND, DEFAULT_FONT
from display.helpers import get_scaled_image, AnimatedObject, CommonSprite, stop_draw, AnimatedObjectV2


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
        self.end_run_screen = EndRunScreen()

        # crafting
        self.crafting_middle_screen = CraftingMiddleScreen()

        # банк/инвентарь (правая панель)
        self.inventory_table = Inventory((1000, 450))
        self.bank_table = Bank((1000, 450))
        self.end_run_button = Button(
            "end_run_button",
            get_scaled_image("sprites/end_run_button.png", 2),
            get_scaled_image("sprites/end_run_button.png", 2),
        )
        self.end_run_button.rect.topleft = (950, 100)
        self.clock = Clock((900, 50))

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

        # главная панель
        self.render_common_ui()

        # основной экран
        if self.page == self.MINING_PAGE:
            self.mining_middle_screen.draw(self.main_surface)

            # TODO: двойная проверка?
            if self.pickaxe.image != stop_draw:
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

            # TODO: двойная проверка?
            if self.end_run_screen.image != stop_draw:
                self.end_run_screen.draw(self.main_surface)
        elif self.page == self.CRAFTING_PAGE:
            self.crafting_middle_screen.draw(self.main_surface)

        # банк/инвентарь (правая панель)
        self.inventory_table.draw(self.main_surface)
        self.bank_table.draw(self.main_surface)
        self.end_run_button.draw(self.main_surface)
        self.clock.draw(self.main_surface)

    def highlight_text(self, item_name, coords):
        # TODO: вот же пример исчезающего объекта, надо сделать как тут
        self.highlight_text_objects.append(LiftingText(f"+1 {item_name}", coords))

    def get_animated_objects(self) -> list[AnimatedObject]:
        result = [self.pickaxe] + self.highlight_text_objects + [self.end_run_screen]
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

    def run_end_run_screen(self):
        self.end_run_screen.start()


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        name: str,
        image_on,
        image_off,
        on: bool = False
    ):
        super().__init__()  # TODO: надо?
        self.name = name  # TODO: а это?
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
            # 39: stop_draw,
        }

        self.rect = None
        self.image = self.pickaxe_idle_image
        self.set_coords((0, 0))
        self.image = stop_draw

    # def add_animation_count(self):
    #     if image := self.frame_image.get(self.animation_count):
    #         self.image = image
    #     self.animation_count += 1
    #
    # def draw(self, surface):
    #     if self.image is stop_draw:
    #         return
    #
    #     surface.blit(self.image, self.rect)

    def do_pickaxe_hit(self, coords):
        self.animation_count = 0
        self.image = self.pickaxe_idle_image
        self.set_coords(coords)

    def set_coords(self, coords):
        rect = self.image.get_rect()
        rect.bottomleft = coords
        self.rect = rect


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


# class DisplayQueue:
#
#     def __init__(self, background_layer, front_layer):
#         self.background_layer = Layer(
#
#         )
#         self.front_layer = Layer(
#
#         )
#
#     def draw(self, surface):
#         surface.blit(self.image, self.rect)
#
#     def add_sprite(self):
#         pass
#
#     def remove_sprite(self):
#         pass
#
#
# class Layer:
#     def __init__(self):
#         pass
#
#     def add_sprite(self):
#         pass
#
#     def remove_sprite(self):
#         pass

