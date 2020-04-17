"""Main module for the cribbage package"""

from cribbage.__init__ import Deck, Player, Computer

# Build the deck
deck = Deck()
deck.populate()
deck.shuffle()

full_deck= deck

# Create players
player = Player("Tim")
computer = Computer(difficulty="easy")

deck.deal(player.hand, computer.hand)

player_discards = player.discard()

player.hand.display_cards()

computer.set_full_deck(full_deck=full_deck)
computer.discard()

shared_card = deck.draw_card()
print(f"Shared card: {shared_card.unicode}")

score = player.hand.score_hand(shared_card=shared_card)

print(score)
