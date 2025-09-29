import pygame

from display import Button


class ActionManager:
    """
    Обработчик всяких разных событий на клиенте
    """

    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.panel = SelectorUI(main_controller.display_manager.buttons)

    def get_hovered_object(self):
        """Возвращает спрайт, над которым в текущий момент находится курсор."""
        for button in self.panel.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                return button

        # self.main_controller.display_manager.

        return None

    def handle_routine(self):
        """
        Обрабатывает ежефреймные события
        """
        # self.handle_mouse_hover()
        pass

    def handle_mouse_click(self):
        """
        Обрабатывает событие left mouse click
        """
        obj = self.get_hovered_object()
        if obj in self.panel.buttons:
            self.panel.set_active_button(obj)



class SelectorUI:
    """
    Абстрактный класс селектор, отвечающий за логику, но не отвечающий за отображение.
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
