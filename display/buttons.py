import pygame

from display.bank import Bank, NotEnough
from display.helpers import CommonSprite, get_scaled_image
from items import (
    Coal,
    GoldenIngot,
    GoldenOre,
    IronIngot,
    IronOre,
    LavaIngot,
    LavaOre,
    PoorIronOre,
    SilverIngot,
    SilverOre,
)


class Button(pygame.sprite.Sprite):
    def __init__(self, name: str, image_on, image_off, on: bool = False):
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
