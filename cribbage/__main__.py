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

cards_to_remove = [player_hand.cards[0], player_hand.cards[5]]

for i in cards_to_remove:

    player_hand.remove_card(i)

player_hand.display_cards()

shared_card = deck.draw_card()
print(shared_card.unicode)

score = player_hand.score_hand(shared_card=shared_card)

print(score)
