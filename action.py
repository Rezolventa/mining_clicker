import random

import pygame

from consts import TICKS_PER_SECOND
from display.helpers import get_random_point_in_circle
from display.manager import Button
from items import IronIngot

from typing import TYPE_CHECKING

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

        self.alarms = []

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
            if self.display_manager.end_run_button.rect.collidepoint(pygame.mouse.get_pos()):
                return self.display_manager.end_run_button
        elif self.display_manager.page == self.display_manager.CRAFTING_PAGE:
            if self.display_manager.crafting_middle_screen.crafting_recipe_image.rect.collidepoint(pygame.mouse.get_pos()):
                return self.display_manager.crafting_middle_screen.crafting_recipe_image

        return None

    def handle_routine(self):
        """
        Обрабатывает ежефреймные события
        """
        self.display_manager.add_animation_count()
        for alarm in self.alarms:
            alarm.handle_routine()
            if alarm.event == "end_run_screen" and alarm.went_off:
                craft_button = self.panel.buttons[1]
                self.panel.set_active_button(craft_button)
                self.display_manager.page = str(craft_button).split("_")[0]
                self.alarms.remove(alarm)

    def handle_mouse_click(self):
        """
        Обрабатывает событие left mouse click
        """
        obj = self.get_hovered_object()
        if obj in self.panel.buttons:
            self.panel.set_active_button(obj)
            self.display_manager.page = str(obj).split("_")[0]

        if self.display_manager.page == self.display_manager.MINING_PAGE:
            if obj == self.display_manager.middle_screen_background_image:
                # TODO: sprite_queue, 2 x layers
                # ПЕРВЫЙ ЭТАП
                # Определение места попадания
                # Запуск анимации кирки
                # Проверка коллизии с кружочками
                #
                # ВТОРОЙ ЭТАП
                # Отрисовка кружочка
                # Вычисление дропа
                # Добавление дропа в банк
                # Вывод текста с дропом

                # TODO: убрать в отдельный метод hit_circle.on_click() или типа того
                unlucky_drop = False
                mouse_pos = pygame.mouse.get_pos()
                for hit_circle in self.display_manager.pickaxe_hit_circles:
                    if hit_circle.rect.collidepoint(mouse_pos):
                        pos_in_mask = mouse_pos[0] - hit_circle.rect.x, mouse_pos[1] - hit_circle.rect.y
                        if hit_circle.mask.get_at(pos_in_mask):
                            unlucky_drop = True
                            break

                dropped_item = DropChanceManager().get_drop(unlucky_drop)
                row = self.display_manager.inventory_table.get_row(dropped_item)
                dropped_quantity = 1
                row.add_quantity(dropped_quantity)

                random_coords = get_random_point_in_circle(
                    pygame.mouse.get_pos()[0],
                    pygame.mouse.get_pos()[1],
                    15,
                )
                self.display_manager.add_hit_circle(random_coords)
                self.display_manager.pickaxe.do_pickaxe_hit(random_coords)
                self.display_manager.highlight_text(str(row.item.highlight_text), pygame.mouse.get_pos())
            elif obj == self.display_manager.end_run_button:
                end_run_screen_alarm = Alarm("end_run_screen", 50)
                self.alarms.append(end_run_screen_alarm)
                self.display_manager.run_end_run_screen()

                # craft_button = self.panel.buttons[1]
                # self.panel.set_active_button(craft_button)
                # self.display_manager.page = str(craft_button).split("_")[0]

        elif self.display_manager.page == self.display_manager.CRAFTING_PAGE:
            if obj == self.display_manager.crafting_middle_screen.crafting_recipe_image:
                row = self.display_manager.bank_table.get_row(IronIngot.slug)
                row.add_quantity(1)


class SelectorUI:
    """
    Абстрактный класс селектор, отвечающий за логику, но не за отображение.
    Из всех элементов активен может быть только один.
    """
    def __init__(self, buttons):
        self.buttons = buttons
        self.active_button = None

    def set_active_button(self, new_active_button: Button):
        for button in self.buttons:
            if button == new_active_button:
                button.on = True
            else:
                button.on = False
            button.update()

        self.active_button = new_active_button


# TODO: заготовка :)
class DropChanceManager:
    loot_table = {
        "iron_ore": 15,
        "poor_iron_ore": 85,
    }

    def __init__(self):
        pass

    def get_drop(self, unlucky_drop):
        roll = random.randint(1, 100)
        if unlucky_drop:
            return "poor_iron_ore"

        if roll <= self.loot_table["iron_ore"]:
            return "iron_ore"
        return "poor_iron_ore"


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
        # self.on = True

    def handle_routine(self):
        # if self.on:
        self.count -= 1

        # if self.count == 0:
        #     self.on = False

    @property
    def went_off(self):
        return self.count == 0
