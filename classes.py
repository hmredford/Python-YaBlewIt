import random

colors = ("red", "orange", "yellow", "green", "blue", "purple")


class Player:
    def __init__(self, name, curse_color):
        self.name = name
        self.curse_color = curse_color
        self.stash = [Card("faulty detonator", "action")]
        self.gems = []
        self.protected_colors = []

    def gain(self, cards):
        for card in cards:
            if card.type == "gem":
                self.gems.append(card)
                # print(f"{card.name} added to pile")
            else:
                self.stash.append(card)
                # print(f"{card.name} added to stash")

    def roll(self):
        return random.randint(1, 8)

    def getstash(self):
        return self.stash

    def getgems(self):
        return self.gems

    def assignvault(self, color):
        self.protected_colors.append(color)

    def clearcolors(self):
        self.protected_colors = []

    def explode(self, value):
        for gem in self.gems:
            if gem.values[0] == value and gem.color not in self.protected_colors:
                self.gems.remove(gem)
            if len(gem.values) == 2:
                if gem.values[1] == value and gem.color not in self.protected_colors:
                    self.gems.remove(gem)
                print(f"{gem.name} exploded!")


class Card:

    def __init__(self, name, type):
        self.type = type
        self.name = name


class Gem(Card):
    def __init__(self, name, type, color, is_double, values):
        super().__init__(name, type)
        self.name = name
        self.type = type
        self.color = color
        self.is_double = is_double
        self.values = values



