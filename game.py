import random
import sys
from classes import Player
from classes import Card
from classes import Gem


class Game:
    def __init__(self):
        self.num_players = 0
        self.players = []
        self.curse_deck = ["red", "orange", "yellow", "green", "blue", "purple"]
        self.deck = []
        self.claim = []
        self.prospector = 0
        self.current_player = 1
        self.players_out = []

    def setup(self, num_players):
        self.num_players = num_players
        i = 1
        while i <= num_players:
            color = random.choice(self.curse_deck)
            self.curse_deck.remove(color)
            self.players.append(Player(f"player{i}", color))
            i += 1

    def shuffledeck(self, num):
        i = 0
        while i < num:
            random.shuffle(self.deck)
            i += 1

    def loaddeck(self):
        filepath = "deck.txt"
        with open(filepath, "r") as file:
            line = file.readline()
            while line:
                row = line.split(",")
                if row[0] == "Card":
                    self.deck.append(Card(row[1], row[2]))
                elif row[0] == "Gem":
                    if len(row) == 6:
                        self.deck.append(Gem(row[1], row[2], row[3], bool(row[4]), [int(row[5])]))
                    elif len(row) == 7:
                        values = [int(row[5]), int(row[6])]
                        self.deck.append(Gem(row[1], row[2], row[3], bool(row[4]), values))
                line = file.readline()
            for player in self.players:
                self.deck.pop()
        self.shuffledeck(7)
        self.deck.insert(0, Card("fire in the hole", "action"))
        print("Deck loaded.")

    def advprospector(self):
        self.prospector = (self.prospector + 1) % self.num_players

    def fireinthehole(self):
        print("\nFIRE IN THE HOLE!\n")
        for player in self.players:
            roll = player.roll()
            print(f"{player.name} rolled a {roll}!\n")
            for gem in player.gems:
                if roll in gem.values:
                    print("\033[91m {}\033[00m" .format(f"BOOM! - {gem.name}"))
                    player.gems.remove(gem)
        self.printstats()

    def addcardtoclaim(self):
        try:
            if len(self.deck) > 1 and self.deck[-1].name != "fire in the hole":
                self.claim.append(self.deck[-1])
                self.deck.pop()
                return True
            else:
                self.deck.pop()
                self.fireinthehole()
                return False
        except:
            print("last card!")
            self.fireinthehole()
            self.score()
            sys.exit(0)


    def printclaim(self):
        print("Current Claim:")
        message = ""
        for card in self.claim:
            if card.type == "gem":
                message += f" {card.name} {card.values} |"
            else:
                message += f"{card.name} |"
        print(message)

    def addtoclaim(self):
        if self.addcardtoclaim():
            if self.claim[-1].type != "gem":
                while self.claim[-1].type != "gem":
                    self.addtoclaim()
        else:
            self.addtoclaim()

    def newround(self):
        self.players_out.clear()

    def stealclaim(self, roll):
        print(f"{self.players[self.current_player].name} rolled {roll}")
        count = 0
        for card in self.claim:
            if card.type == "gem":
                for num in card.values:
                    if num == roll:
                        count += 1
        if count > 0:
            return True
        else:
            return False

    def askplayers(self):
        self.current_player = (self.prospector + 1) % self.num_players
        while len(self.players_out) < (self.num_players - 1):
            if self.current_player != self.prospector:
                if self.players[self.current_player] not in self.players_out:
                    command = input(f"{self.players[self.current_player].name}, would you like to roll for the claim? (y)es/(n)o: ")
                    if command == "y":
                        roll = self.players[self.current_player].roll()
                        if self.stealclaim(roll):
                            print("\nclaim stolen!\n")
                            self.players[self.current_player].gain(self.claim)
                            self.claim = []
                            return True
                        else:
                            self.players_out.append(self.players[self.current_player])
                            print("Missed!")
                        self.current_player = (self.current_player + 1) % self.num_players
                    elif command == "n":
                        self.current_player = (self.current_player + 1) % self.num_players
                    else:
                        print("invalid input.")
                else:
                    self.current_player = (self.current_player + 1) % self.num_players
            else:
                command = input("Prospector, would you like to (t)ake the claim, or (a)dd another gem?: ")
                if command == "t":
                    print("Prospector took claim!")
                    self.players[self.prospector].gain(self.claim)
                    self.claim = []
                    return True
                if command == "a":
                    print(f"Prospector added to claim! {self.players[self.prospector].name} is the Prospector" )
                    self.addtoclaim()
                    self.printclaim()
                    self.current_player = (self.current_player + 1) % self.num_players
        return False

    def askgamble(self):
        print("All players out!")
        self.printclaim()
        command = input(f"{self.players[self.prospector].name}, would you like to (t)ake the claim, or (g)amble?: ")
        if command == "t":
            print("Prospector took claim!")
            self.players[self.prospector].gain(self.claim)
            self.claim = []
        elif command == "g":
            self.addtoclaim()
            self.printclaim()
            command = input("Would you like to add another card? (y)es or (n)o?: ")
            if command == "y":
                self.addtoclaim()
                self.printclaim()
            roll = self.players[self.current_player].roll()
            if not self.stealclaim(roll):
                print("claim stolen!")
                self.players[self.prospector].gain(self.claim)
                self.claim = []
            else:
                print("Missed! Claim exploded!")
                self.claim = []

    def printstats(self):
        for player in self.players:
            stash = ""
            for card in player.stash:
                stash += f"{card.name} | "
            gems = ""
            for gem in player.gems:
                gems += f"{gem.name} {gem.values} | "
            print(f"{player.name}'s stash: {stash} gems: {gems}")

    def score(self):
        print("\nEnd of game!\n")
        colors = ("red", "orange", "yellow", "green", "blue", "purple")
        for player in self.players:
            print(f"\n{player.name}'s Score:")
            for color in colors:
                count = 0
                for gem in player.gems:
                    if gem.color == color:
                        if gem.is_double:
                            count += 2
                        else:
                            count += 1
                print(f"Total {color} gems: {count}")


    def begin(self):
        while len(self.deck) > 1:
            self.newround()
            self.addtoclaim()
            self.printstats()
            print(f"\n{self.players[self.prospector].name} is the prospector! (deck:{len(self.deck)})")
            self.printclaim()
            if not self.askplayers():
                self.askgamble()
            self.advprospector()
        self.score()
