from consts import WHITE, DEFAULT_FONT
from display.helpers import get_scaled_image
from items import PoorIronOre, IronOre, IronIngot, Coal, SilverOre, GoldenOre, LavaOre, SilverIngot, GoldenIngot, \
    LavaIngot


class ObjectRowIconAndText:
    def __init__(self, item, bottom_left_coords):
        self.item = item
        self.icon = get_scaled_image(item.image_url, item.scale)
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


class ItemTable:
    space_between_rows_px = None
    space_between_columns_px = None
    item_table = None

    def __init__(self, initial_top_left_coords):
        self.top_left_coords = initial_top_left_coords
        self.display_table = []

        for item_list in self.item_table:
            column = []
            for item in item_list:
                self.top_left_coords = (self.top_left_coords[0], self.top_left_coords[1] + self.space_between_rows_px)
                column.append(ObjectRowIconAndText(item, self.top_left_coords))
            self.display_table.append(column)

            # переходим на следующий столбец
            self.top_left_coords = (
                initial_top_left_coords[0] + self.space_between_columns_px, initial_top_left_coords[1]
            )

    def draw(self, surface):
        for column in self.display_table:
            for row in column:
                if row.quantity > 0:
                    row.draw(surface)

    # не используется?
    def get_row(self, item_slug: str) -> ObjectRowIconAndText:
        for column in self.display_table:
            for row in column:
                if row.item.slug == item_slug:
                    return row


class Bank(ItemTable):
    space_between_rows_px = 30
    space_between_columns_px = 100
    item_table = [
        [PoorIronOre, IronOre, Coal, SilverOre, GoldenOre, LavaOre],
        [IronIngot, Coal, SilverIngot, GoldenIngot, LavaIngot],
    ]


class Inventory(ItemTable):
    space_between_rows_px = 30
    space_between_columns_px = 100
    item_table = [
        [PoorIronOre, IronOre, Coal, SilverOre, GoldenOre, LavaOre],
        [IronIngot, Coal, SilverIngot, GoldenIngot, LavaIngot],
    ]
