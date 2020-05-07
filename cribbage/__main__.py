"""Main module for the cribbage package"""

from copy import copy
from cribbage.__init__ import Deck, Player, Computer

# Build the deck
deck = Deck()
deck.populate()
deck.shuffle()

all_cards = copy(deck.cards)

player = Player("Tim")
computer = Computer("hard")

computer.add_cards_list(all_cards)

player.give_crib()

deck.deal(player.hand, computer.hand)

player_discards = player.discard()
computer_discards = computer.discard()

shared_card = deck.draw_card()

print(shared_card.unicode)
player.hand.display_cards()
computer.hand.display_cards()

player_score = player.hand.score_hand(shared_card=shared_card)
computer_score = computer.hand.score_hand(shared_card=shared_card)

print(player_score)
print(computer_score)

print([i.unicode for i in player_discards])
print([i.unicode for i in computer_discards])
