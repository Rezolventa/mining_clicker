import random

import pygame

from consts import TICKS_PER_SECOND
from display.bank import merge_inventory_to_bank
from display.helpers import get_random_point_in_circle
from display.manager import SelectorUI
from items import IronIngot, Item, PoorIronOre, IronOre, Coal

from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from client import MainController


class ActionManager:
    """
    Обработчик всяких разных событий на клиенте
    """

    def __init__(self, main_controller: "MainController"):
        self.main_controller = main_controller
        self.display_manager = main_controller.display_manager
        self.panel = SelectorUI(self.display_manager.buttons)

        # текущий основной экран
        self.middle_screen = self.display_manager.mining_middle_screen
        self.pickaxe = self.display_manager.pickaxe

        self.alarms: list[Alarm] = []

    def get_hovered_object(self):
        """
        Возвращает объект, над которым в текущий момент находится курсор
        """
        for button in self.panel.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                return button

        if self.display_manager.page == self.display_manager.MINING_PAGE:
            if self.display_manager.middle_screen_background_image.rect.collidepoint(pygame.mouse.get_pos()):
                return self.display_manager.middle_screen_background_image

            """    
            Для MVP выход из рейда и время не делаем
            if self.display_manager.end_run_button.rect.collidepoint(pygame.mouse.get_pos()):
                return self.display_manager.end_run_button
            """

        elif self.display_manager.page == self.display_manager.CRAFTING_PAGE:
            for crafting_item in self.display_manager.crafting_middle_screen.group:
                if crafting_item.rect.collidepoint(pygame.mouse.get_pos()):
                    return crafting_item

        return None

    def handle_routine(self):
        """
        Обрабатывает ежефреймные события
        """
        self.display_manager.add_animation_count()
        self.handle_alarms()

    def handle_alarms(self):
        for alarm in self.alarms:
            alarm.handle_routine()

            """    
            Для MVP выход из рейда и время не делаем
            if alarm.went_off and alarm.event == "end_run_screen":
                # сработал будильник - переключаем на вкладку Craft
                craft_button = self.panel.buttons[1]
                self.panel.set_active_button(craft_button)
                self.display_manager.page = str(craft_button).split("_")[0]
                self.alarms.remove(alarm)
            """

    def is_unlucky(self):
        unlucky_drop = False
        mouse_pos = pygame.mouse.get_pos()
        for hit_circle in self.display_manager.pickaxe_hit_circles:
            if hit_circle.rect.collidepoint(mouse_pos):
                pos_in_mask = mouse_pos[0] - hit_circle.rect.x, mouse_pos[1] - hit_circle.rect.y
                if hit_circle.mask.get_at(pos_in_mask):
                    unlucky_drop = True
                    break
        return unlucky_drop

    def do_pickaxe_hit(self):
        """
        ПЕРВЫЙ ЭТАП
        Определение места попадания
        Запуск анимации кирки
        Проверка коллизии с кружочками

        ВТОРОЙ ЭТАП
        Отрисовка кружочка
        Вычисление дропа
        Добавление дропа в банк
        Вывод текста с дропом
        """
        dropped_item = self.add_drop()

        random_coords = get_random_point_in_circle(
            pygame.mouse.get_pos()[0],
            pygame.mouse.get_pos()[1],
            15,
        )
        self.display_manager.add_hit_circle(random_coords)
        self.display_manager.pickaxe.start(random_coords)
        self.display_manager.highlight_text(str(dropped_item.highlight_text), pygame.mouse.get_pos())

    def add_drop(self):
        unlucky_drop = self.is_unlucky()
        dropped_item = DropChanceManager().get_drop(unlucky_drop)
        dropped_quantity = 1

        self.display_manager.inventory_table.add_drop(dropped_item, dropped_quantity)
        return dropped_item

    def handle_mouse_click(self):
        """
        Обрабатывает событие left mouse click
        """
        obj = self.get_hovered_object()
        if obj in self.panel.buttons:
            self.panel.set_active_button(obj)
            self.display_manager.page = str(obj).split("_")[0]

            if obj == self.panel.buttons[0]:
                self.display_manager.clear_mining_screen()
            elif obj == self.panel.buttons[1]:
                merge_inventory_to_bank(self.display_manager.inventory_table, self.display_manager.bank_table)

        if self.display_manager.page == self.display_manager.MINING_PAGE:
            if obj == self.display_manager.middle_screen_background_image:
                self.do_pickaxe_hit()

            """
            Для MVP выход из рейда и время не делаем
            elif obj == self.display_manager.end_run_button:
                end_run_screen_alarm = Alarm("end_run_screen", 50)
                self.alarms.append(end_run_screen_alarm)
                self.display_manager.run_end_run_screen()
            """

        elif self.display_manager.page == self.display_manager.CRAFTING_PAGE:
            if obj in self.display_manager.crafting_middle_screen.group:
                obj.on_click(self.display_manager.bank_table)


class MiningPageManager:
    pass


class CraftingPageManager:
    pass


class DropChanceManager:
    loot_table = {
        "poor_iron_ore": 60,
        "iron_ore": 15,
        "coal": 25,
    }

    def __init__(self):
        pass

    def get_drop(self, unlucky_drop: bool) -> Type[Item]:
        roll = random.randint(1, 100)
        if unlucky_drop:
            return PoorIronOre

        if roll <= self.loot_table["iron_ore"]:
            return IronOre
        elif self.loot_table["iron_ore"] <= roll < self.loot_table["iron_ore"] + self.loot_table["coal"]:
            return Coal
        return PoorIronOre


class TimeManager:
    def __init__(self):
        self.ticks_per_game_hour = TICKS_PER_SECOND * 3
        self.hour = 0
        self.day = 1
        self.tick = 0

    def handle_routine(self):
        self.tick += 1
        if self.tick == self.ticks_per_game_hour:
            self.hour += 1
            self.tick = 0

        if self.hour == 24:
            self.day += 1
            self.hour = 0


class Alarm:
    def __init__(self, event, count):
        self.event = event
        self.count = count

    def handle_routine(self):
        self.count -= 1

    @property
    def went_off(self):
        return self.count == 0
