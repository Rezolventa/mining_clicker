

class Item:
    name = None
    slug = None
    image_url = None
    scale = 1
    order_number = 0


class PoorIronOre(Item):
    name = "Poor Iron Ore"
    slug = "poor_iron_ore"
    image_url = "sprites/poor_iron_ore.png"
    highlight_text = "poor iron ore"
    scale = 2
    order_number = 1


class IronOre(Item):
    name = "Iron Ore"
    slug = "iron_ore"
    image_url = "sprites/iron_ore.png"
    highlight_text = "iron ore"
    scale = 2
    order_number = 2


class Coal(Item):
    name = "Coal"
    slug = "coal"
    image_url = "sprites/coal.png"
    highlight_text = "coal"
    scale = 2
    order_number = 3


class SilverOre(Item):
    name = "Silver Ore"
    slug = "silver_ore"
    image_url = "sprites/silver_ore.png"
    highlight_text = "silver ore"
    scale = 2
    order_number = 4


class GoldenOre(Item):
    name = "Golden Ore"
    slug = "golden_ore"
    image_url = "sprites/golden_ore.png"
    highlight_text = "golden ore"
    scale = 2
    order_number = 5


class LavaOre(Item):
    name = "Lava Ore"
    slug = "lava_ore"
    image_url = "sprites/lava_ore.png"
    highlight_text = "lava ore"
    scale = 2
    order_number = 6


class IronIngot(Item):
    name = "Iron Ingot"
    slug = "iron_ingot"
    image_url = "sprites/iron_ingot.png"
    highlight_text = "iron ingot"
    order_number = 100


class SilverIngot(Item):
    name = "Silver Ingot"
    slug = "silver_ingot"
    image_url = "sprites/silver_ingot.png"
    highlight_text = "silver ingot"
    order_number = 101


class GoldenIngot(Item):
    name = "Golden Ingot"
    slug = "golden_ingot"
    image_url = "sprites/golden_ingot.png"
    highlight_text = "golden ingot"
    order_number = 102


class LavaIngot(Item):
    name = "Lava Ingot"
    slug = "lava_ingot"
    image_url = "sprites/lava_ingot.png"
    highlight_text = "lava ingot"
    order_number = 103
