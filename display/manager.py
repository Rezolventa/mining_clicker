from typing import Type

import pygame
from pygame.sprite import Sprite

from display.bank import Bank, Inventory, merge_inventory_to_bank, NotEnough
from consts import WHITE, SCREEN_WIDTH, SCREEN_HEIGHT, TICKS_PER_SECOND, DEFAULT_FONT
from display.helpers import get_scaled_image, AnimatedObject, CommonSprite, stop_draw, AnimatedObjectV2
from items import PoorIronOre, Coal, IronIngot, IronOre, SilverOre, SilverIngot, GoldenIngot, GoldenOre, LavaOre, \
    LavaIngot, Gold


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

        # Основной экран
        # mining
        self.mining_middle_screen = MiningMiddleScreen()
        self.pickaxe = PickaxeHit()
        self.highlight_text_objects: list[LiftingText] = []
        self.pickaxe_hit_circles = []

        # crafting
        self.crafting_middle_screen = CraftingMiddleScreen()

        # банк/инвентарь (правая панель)
        self.inventory_table = Inventory((1000, 450))
        self.bank_table = Bank((1000, 450))
        self.bank_table.add_drop(PoorIronOre, 350)
        self.bank_table.add_drop(IronOre, 350)
        self.bank_table.add_drop(Coal, 1500)
        self.bank_table.add_drop(SilverOre, 250)
        self.bank_table.add_drop(GoldenOre, 150)
        self.bank_table.add_drop(LavaOre, 25)
        self.gold = 0

        """    
        Для MVP выход из рейда и время не делаем
        self.end_run_screen = EndRunScreen()
        self.end_run_button = Button(
            "end_run_button",
            get_scaled_image("sprites/end_run_button.png", 2),
            get_scaled_image("sprites/end_run_button.png", 2),
        )
        self.end_run_button.rect.topleft = (950, 100)
        self.clock = Clock((900, 50))
        """

        self.sell_page_manager = SellPageManager()

    def init_panel_buttons(self):
        # TODO: унаследоваться от общего класса
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
        self.render_common_ui()

        # основной экран
        if self.page == self.MINING_PAGE:
            self.render_mining_page()
        elif self.page == self.CRAFTING_PAGE:
            self.render_craft_page()
        elif self.page == self.VENDOR_PAGE:
            self.render_vendor_page()

        self.render_right_panel()

        """    
        Для MVP выход из рейда и время не делаем
        self.end_run_button.draw(self.main_surface)
        self.clock.draw(self.main_surface)
        """

    def render_mining_page(self):
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

        """    
        Для MVP выход из рейда и время не делаем
        # TODO: двойная проверка?
        if self.end_run_screen.image != stop_draw:
            self.end_run_screen.draw(self.main_surface)
        """

    def render_craft_page(self):
        self.crafting_middle_screen.draw(self.main_surface)

    def render_vendor_page(self):
        self.sell_page_manager.draw(self.main_surface)

    def render_right_panel(self):
        if self.page == self.MINING_PAGE:
            self.inventory_table.draw(self.main_surface)
        else:
            self.bank_table.draw(self.main_surface)

        gold_text = DEFAULT_FONT.render(f"Gold: {self.gold}", True, WHITE)
        self.main_surface.blit(gold_text, (1000, 80))

    def add_gold(self, quantity):
        self.gold += quantity

    def highlight_text(self, item_name, coords):
        # TODO: вот же пример исчезающего объекта, надо сделать как тут
        self.highlight_text_objects.append(LiftingText(f"+1 {item_name}", coords))

    def get_animated_objects(self) -> list[Type[AnimatedObject]]:
        """
        Для MVP выход из рейда и время не делаем
        result = [self.pickaxe] + self.highlight_text_objects + [self.end_run_screen]
        """

        result = [self.pickaxe] + self.highlight_text_objects
        return result

    def add_animation_count(self):
        # TODO: каждый раз вычислять get_animated_objects это не оптимально
        for obj in self.get_animated_objects():
            obj.add_animation_count()

    def add_hit_circle(self, center_coords):
        self.pickaxe_hit_circles.append(HitCircle(center_coords))

    def clear_mining_screen(self):
        self.inventory_table.clear()
        self.pickaxe_hit_circles = []
        self.highlight_text_objects = []

    """    
    Для MVP выход из рейда и время не делаем
    def run_end_run_screen(self):
        self.end_run_screen.start()
        merge_inventory_to_bank(self.inventory_table, self.bank_table)
    """


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
        self.middle_screen_background_image = get_scaled_image("sprites/mining_background_2.png", 2)

    def draw(self, surface):
        surface.blit(self.middle_screen_background_image, (241, 10))


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


class TransactionButton(CommonSprite):
    _image = None
    credit = dict()
    debit = dict()

    def __init__(self):
        super().__init__(get_scaled_image(self._image, 3))

    def make_transaction(self, bank_table: Bank):
        pass

    def on_click(self, bank_table: Bank):
        return self.make_transaction(bank_table)


class CraftingRecipeButton(TransactionButton):
    def make_transaction(self, bank_table: Bank):
        old_values = dict()

        try:
            self.do_credit(bank_table, old_values)
        except NotEnough:
            self.rollback(bank_table, old_values)
            return

        self.do_debit(bank_table)

    @staticmethod
    def rollback(bank_table: Bank, old_values: dict):
        for item, quantity in old_values.items():
            row = bank_table.get_row(item)
            row.set_quantity(quantity)

    def do_credit(self, bank_table: Bank, old_values: dict):
        for item, quantity in self.credit.items():
            row = bank_table.get_row(item)
            old_values[item] = row.quantity  # запоминаем старые значения на случай отката
            row.add_quantity(-quantity)

    def do_debit(self, bank_table: Bank):
        for key, value in self.debit.items():
            row = bank_table.get_row(key)
            row.add_quantity(value)


class PriceTag(CraftingRecipeButton):
    price = None

    def make_transaction(self, bank_table: Bank):
        old_values = dict()

        try:
            self.do_credit(bank_table, old_values)
        except NotEnough:
            self.rollback(bank_table, old_values)
            return 0

        return self.do_debit(bank_table)

    def do_debit(self, bank_table: Bank):
        return self.price


class PoorIronIngotButton(CraftingRecipeButton):
    _image = "sprites/crafting_poor_iron_ingot.png"

    credit = {
        PoorIronOre: 8,
        Coal: 3,
    }

    debit = {
        IronIngot: 1,
    }


class IronIngotButton(CraftingRecipeButton):
    _image = "sprites/crafting_iron_ingot.png"

    credit = {
        IronOre: 2,
        Coal: 1,
    }

    debit = {
        IronIngot: 1,
    }


class SilverIngotButton(CraftingRecipeButton):
    _image = "sprites/crafting_silver_ingot.png"

    credit = {
        SilverOre: 2,
        Coal: 15,
    }

    debit = {
        SilverIngot: 1,
    }


class GoldenIngotButton(CraftingRecipeButton):
    _image = "sprites/crafting_golden_ingot.png"

    credit = {
        GoldenOre: 2,
        Coal: 4,
    }

    debit = {
        GoldenIngot: 1,
    }


class LavaIngotButton(CraftingRecipeButton):
    _image = "sprites/crafting_lava_ingot.png"

    credit = {
        LavaOre: 1,
        Coal: 80,
    }

    debit = {
        LavaIngot: 1,
    }


class SellIronIngotButton(PriceTag):
    _image = "sprites/sell_iron_ingot.png"
    price = 2

    credit = {
        IronIngot: 1,
    }


class SellSilverIngotButton(PriceTag):
    _image = "sprites/sell_silver_ingot.png"
    price = 25

    credit = {
        SilverIngot: 1,
    }


class SellGoldenIngotButton(PriceTag):
    _image = "sprites/sell_golden_ingot.png"
    price = 50

    credit = {
        GoldenIngot: 1,
    }


class SellLavaIngotButton(PriceTag):
    _image = "sprites/sell_lava_ingot.png"
    price = 1500

    credit = {
        LavaIngot: 1,
    }


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


class SelectorUI:
    """
    Из всех элементов активен может быть только один.
    """
    def __init__(self, buttons: list[Button]):
        self.buttons = buttons
        self.active_button = None

    def set_active_button(self, new_active_button: Button) -> None:
        for button in self.buttons:
            if button == new_active_button:
                button.on = True
            else:
                button.on = False
            button.update()

        self.active_button = new_active_button


class MiningPageManager:
    pass


class CraftingPageManager:
    pass


class SellPageManager:
    def __init__(self):
        self.sell_iron_ingot = SellIronIngotButton()
        self.sell_iron_ingot.rect.topleft = (300, 250)

        self.sell_silver_ingot = SellSilverIngotButton()
        self.sell_silver_ingot.rect.topleft = (450, 250)

        self.sell_golden_ingot = SellGoldenIngotButton()
        self.sell_golden_ingot.rect.topleft = (600, 250)

        self.sell_lava_ingot = SellLavaIngotButton()
        self.sell_lava_ingot.rect.topleft = (300, 400)

        self.group = [
            self.sell_iron_ingot,
            self.sell_silver_ingot,
            self.sell_golden_ingot,
            self.sell_lava_ingot,
        ]

    def draw(self, surface):
        for sprite in self.group:
            sprite.draw(surface)
