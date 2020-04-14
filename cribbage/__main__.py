"""Main module for the cribbage package"""

from cribbage.__init__ import Deck, Hand

# Build the deck
deck = Deck()
deck.populate()
deck.shuffle()

# Build hands
player_hand = Hand()
computer_hand = Hand()
crib = Hand(is_crib=True)

deck.deal(player_hand, computer_hand)

player_hand.display_cards()
