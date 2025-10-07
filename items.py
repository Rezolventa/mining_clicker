

class Item:
    name = None
    slug = None
    image_url = None


class PoorIronOre(Item):
    name = "Poor Iron Ore"
    slug = "poor_iron_ore"
    image_url = "sprites/1.png"


class IronOre(Item):
    name = "Iron Ore"
    slug = "iron_ore"
    image_url = "sprites/2.png"