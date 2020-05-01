"""Main module for the cribbage package"""

from cribbage.__init__ import Deck, Player, Computer

# Build the master deck reference
deck = Deck()
deck.populate()

all_cards = deck.cards

deck.draw_card()

print(type(deck.cards))
print(type(all_cards))

#computer.discard()
