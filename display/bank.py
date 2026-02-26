from consts import WHITE, DEFAULT_FONT
from display.helpers import get_scaled_image
from items import PoorIronOre, IronOre, IronIngot


class ObjectRowIconAndText:
    def __init__(self, item, bottom_left_coords):
        self.item = item
        self.icon = get_scaled_image(item.image_url)
        self.icon_rect = self.icon.get_rect()
        self.icon_rect.bottomleft = bottom_left_coords

        self.quantity = 0

        self.text_image = DEFAULT_FONT.render("x0", True, WHITE)
        self.text_rect = self.text_image.get_rect()
        self.text_rect.bottomleft = (self.icon_rect.bottomleft[0] + 30, self.icon_rect.bottomleft[1])

    def draw(self, surface):
        surface.blit(self.icon, self.icon_rect)
        surface.blit(self.text_image, self.text_rect)

    def add_quantity(self, quantity):
        self.quantity += quantity
        text_rect = self.text_rect
        self.text_image = DEFAULT_FONT.render("x" + str(self.quantity), True, WHITE)
        self.text_rect = text_rect

    def __repr__(self):
        return self.item.slug


class BankTable:
    space_between_rows_px = 30

    def __init__(self, top_left_coords):
        self.top_left_coords = top_left_coords
        self.items_list = [PoorIronOre, IronOre, IronIngot]
        # TODO: может это должен быть dict?
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