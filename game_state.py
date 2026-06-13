import random

from consts import ENABLE_RUNES, RUNE_APPEAR_CHANCE
from display.bank import Bank, Inventory, merge_inventory_to_bank
from items import Coal, GoldenOre, IronOre, LavaOre, PoorIronOre, SilverOre
from runes import RuneChallenge


class GameState:
    MINING_PAGE = "mining"
    CRAFTING_PAGE = "crafting"
    VENDOR_PAGE = "vendor"

    def __init__(self):
        self.current_page = self.MINING_PAGE
        self.inventory = Inventory((1000, 450))
        self.bank = Bank((1000, 450))
        self.gold = 0
        self.rune_challenge = None
        self.last_rune_score = None

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

    def has_active_rune_challenge(self):
        return ENABLE_RUNES and self.rune_challenge is not None

    def try_start_rune_challenge(self, center_coords):
        if not ENABLE_RUNES or self.rune_challenge is not None:
            return False

        if random.random() >= RUNE_APPEAR_CHANCE:
            return False

        self.rune_challenge = RuneChallenge(center_coords)
        self.last_rune_score = None
        return True

    def add_rune_frame(self):
        if self.has_active_rune_challenge():
            self.rune_challenge.add_frame()

    def handle_rune_click(self, coords):
        if not self.has_active_rune_challenge():
            return False, None

        if not self.rune_challenge.handle_click(coords):
            return False, None

        if not self.rune_challenge.is_completed:
            return True, None

        self.last_rune_score = self.rune_challenge.score
        self.rune_challenge = None
        return True, self.last_rune_score

    def clear_rune_challenge(self):
        self.rune_challenge = None
        self.last_rune_score = None
