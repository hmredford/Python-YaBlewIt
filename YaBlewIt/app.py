import classes
import game
# Setup
game = game.Game()
print("Welcome to python YaBlewIt!")
num_players = input("Please enter the number of players for this game: ")
game.setup(int(num_players))
for player in game.players:
    print(f"Welcome {player.name}!")
game.loaddeck()

# Game play
game.begin()

# Score
#game.score()
