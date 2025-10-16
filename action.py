import random

import pygame

from display import Button


class ActionManager:
    """
    Обработчик всяких разных событий на клиенте
    """

    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.display_manager = main_controller.display_manager
        self.panel = SelectorUI(self.display_manager.buttons)

        self.middle_screen = self.display_manager.middle_screen

    def get_hovered_object(self):
        """
        Возвращает объект, над которым в текущий момент находится курсор
        """
        for button in self.panel.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                return button

        if self.middle_screen.rect.collidepoint(pygame.mouse.get_pos()):
            return self.middle_screen

        return None

    def handle_routine(self):
        """
        Обрабатывает ежефреймные события
        """
        self.middle_screen.add_animation_count()
        self.display_manager.add_animation_count()

    def handle_mouse_click(self):
        """
        Обрабатывает событие left mouse click
        """
        obj = self.get_hovered_object()
        if obj in self.panel.buttons:
            self.panel.set_active_button(obj)
            self.display_manager.page = str(obj).split("_")[0]

        if self.display_manager.page == self.display_manager.MINING_PAGE:
            if obj == self.display_manager.middle_screen:
                obj.do_pickaxe_hit()

                dropped_item = DropChanceManager().get_drop()
                row = self.display_manager.bank_table.get_row(dropped_item)
                dropped_quantity = 1
                row.add_quantity(dropped_quantity)

                self.display_manager.highlight_text(str(row.item.highlight_text), pygame.mouse.get_pos())


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
        "iron_ore": 7,
        "poor_iron_ore": 93,
    }

    def __init__(self):
        pass

    def get_drop(self):
        roll = random.randint(1, 100)
        if roll <= self.loot_table["iron_ore"]:
            return "iron_ore"
        return "poor_iron_ore"
