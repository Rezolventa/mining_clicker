import random

import pygame

from display import Button


class ActionManager:
    """
    Обработчик всяких разных событий на клиенте
    """

    def __init__(self, main_controller):
        self.iron_scrap_count = 0
        self.iron_ore_count = 0

        self.main_controller = main_controller
        self.panel = SelectorUI(main_controller.display_manager.buttons)
        self.main_screen = self.main_controller.display_manager.main_screen

    def get_hovered_object(self):
        """
        Возвращает спрайт, над которым в текущий момент находится курсор
        """
        for button in self.panel.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                return button

        if self.main_screen.rect.collidepoint(pygame.mouse.get_pos()):
            return self.main_screen

        return None

    def handle_routine(self):
        """
        Обрабатывает ежефреймные события
        """
        self.main_screen.add_animation_count()
        self.main_controller.display_manager.add_animation_count()

    def handle_mouse_click(self):
        """
        Обрабатывает событие left mouse click
        """
        obj = self.get_hovered_object()
        if obj in self.panel.buttons:
            self.panel.set_active_button(obj)

        if obj == self.main_controller.display_manager.main_screen:
            obj.do_pickaxe_hit()

            dropped_item = DropChanceManager().get_drop()
            counter = getattr(self, dropped_item + "_count") + 1
            setattr(self, dropped_item + "_count", counter)

            self.main_controller.display_manager.highlight_text(pygame.mouse.get_pos())
            if dropped_item == "iron_scrap":
                self.main_controller.display_manager.iron_scrap_icon_text.change_text(str(counter))
            elif dropped_item == "iron_ore":
                self.main_controller.display_manager.iron_ore_icon_text.change_text(str(counter))


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


class DropChanceManager:
    loot_table = {
        "iron_ore": 7,
        "iron_scrap": 93,
    }

    def __init__(self):
        pass

    def get_drop(self):
        roll = random.randint(1, 100)
        if roll <= self.loot_table["iron_ore"]:
            return "iron_ore"
        return "iron_scrap"