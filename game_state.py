from display.bank import Bank, Inventory, merge_inventory_to_bank
from items import Coal, GoldenOre, IronOre, LavaOre, PoorIronOre, SilverOre


class GameState:
    MINING_PAGE = "mining"
    CRAFTING_PAGE = "crafting"
    VENDOR_PAGE = "vendor"

    def __init__(self):
        self.current_page = self.MINING_PAGE
        self.inventory = Inventory((1000, 450))
        self.bank = Bank((1000, 450))
        self.gold = 0

        self.bank.add_drop(PoorIronOre, 350)
        self.bank.add_drop(IronOre, 350)
        self.bank.add_drop(Coal, 1500)
        self.bank.add_drop(SilverOre, 250)
        self.bank.add_drop(GoldenOre, 150)
        self.bank.add_drop(LavaOre, 25)

    def move_inventory_to_bank(self):
        merge_inventory_to_bank(self.inventory, self.bank)
        self.inventory.clear()

    def clear_inventory(self):
        self.inventory.clear()

    def add_gold(self, quantity):
        self.gold += quantity
