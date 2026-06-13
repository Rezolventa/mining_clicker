from typing import Type

import pygame

from consts import DEFAULT_FONT, ENABLE_HIT_CIRCLES, ENABLE_RUNES, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE
from display.animated import CraftingScreen, LiftingText, PickaxeHit
from display.buttons import (
    Button,
    SellGoldenIngotButton,
    SellIronIngotButton,
    SellLavaIngotButton,
    SellSilverIngotButton,
)
from display.helpers import AnimatedObject, CommonSprite, get_scaled_image
from display.utils import HitCircle
from game_state import GameState


class DisplayManager:
    MINING_PAGE = GameState.MINING_PAGE
    CRAFTING_PAGE = GameState.CRAFTING_PAGE
    VENDOR_PAGE = GameState.VENDOR_PAGE

    def __init__(self, game_state: GameState, main_surface=None):
        self.game_state = game_state
        self.main_surface = main_surface or pygame.display.get_surface()
        if self.main_surface is None:
            self.main_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # TODO: этот CommonSprite на хрен не нужен, лучше в draw напрямую указывать координаты, т.к. это статика
        self.middle_screen_background_image = CommonSprite(get_scaled_image("sprites/middle_screen.png", 4))
        self.middle_screen_background_image.rect.topleft = (236, 0)

        # главная панель
        self.buttons = self.init_panel_buttons()

        # Основной экран
        # mining
        self.mining_screen = MiningScreen()
        self.pickaxe = PickaxeHit()
        self.highlight_text_objects: list[LiftingText] = []
        self.pickaxe_hit_circles = []

        # crafting
        self.crafting_screen = CraftingScreen()

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

        self.sell_screen = SellScreen()

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
        if self.game_state.current_page == self.MINING_PAGE:
            self.render_mining_page()
        elif self.game_state.current_page == self.CRAFTING_PAGE:
            self.render_craft_page()
        elif self.game_state.current_page == self.VENDOR_PAGE:
            self.render_vendor_page()

        self.render_right_panel()

        """    
        Для MVP выход из рейда и время не делаем
        self.end_run_button.draw(self.main_surface)
        self.clock.draw(self.main_surface)
        """

    def render_mining_page(self):
        self.mining_screen.draw(self.main_surface)
        self.pickaxe.draw(self.main_surface)

        # если использовать self.highlight_text_objects, возникает баг отображения при удалении элемента "на лету"
        temp_list = self.highlight_text_objects.copy()
        for obj in temp_list:
            if obj.show:
                obj.draw(self.main_surface)
            else:
                self.highlight_text_objects.remove(obj)

        if ENABLE_HIT_CIRCLES:
            for hit_circle in self.pickaxe_hit_circles:
                hit_circle.draw(self.main_surface)

        self.render_rune_challenge()
        """    
        Для MVP выход из рейда и время не делаем
        # TODO: двойная проверка?
        if self.end_run_screen.image != stop_draw:
            self.end_run_screen.draw(self.main_surface)
        """

    def render_craft_page(self):
        self.crafting_screen.draw(self.main_surface)

    def render_vendor_page(self):
        self.sell_screen.draw(self.main_surface)

    def render_right_panel(self):
        if self.game_state.current_page == self.MINING_PAGE:
            self.game_state.inventory.draw(self.main_surface)
        else:
            self.game_state.bank.draw(self.main_surface)

        gold_text = DEFAULT_FONT.render(f"Gold: {self.game_state.gold}", True, WHITE)
        self.main_surface.blit(gold_text, (1000, 80))

    def render_rune_challenge(self):
        if ENABLE_RUNES and self.game_state.rune_challenge:
            self.game_state.rune_challenge.draw(self.main_surface)

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
        self.pickaxe_hit_circles = []
        self.highlight_text_objects = []

    """    
    Для MVP выход из рейда и время не делаем
    def run_end_run_screen(self):
        self.end_run_screen.start()
        self.game_state.move_inventory_to_bank()
    """


class MiningScreen:
    def __init__(self):
        self.middle_screen_background_image = get_scaled_image("sprites/mining_background_2.png", 2)

    def draw(self, surface):
        surface.blit(self.middle_screen_background_image, (241, 10))


class SellScreen:
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
