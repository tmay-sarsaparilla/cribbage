"""Module for playing a game of cribbage"""

from cribbage.player import Player, Computer
from cribbage.functions import play_hand


def play():
    """Function for playing a game of cribbage"""

    # Create the player and the computer
    # TODO: Prompt user for these inputs
    player = Player(player_name="Tim")
    computer = Computer(difficulty="easy")

    continue_game = True

    # Start the game
    while continue_game:

        # Game will continue until a player wins
        continue_game = play_hand(player=player, computer=computer)

    return
