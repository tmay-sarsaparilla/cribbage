"""Module for defining a deck of cards"""

from random import shuffle
from cribbage.card.define_card import Card, cards_list, suits_list


class Deck:
    """Class for a deck of cards"""

    def __init__(self):

        self.cards = self.populate()

    @staticmethod
    def populate():
        """Method for populating a deck of cards"""

        card_list = []

        for i in suits_list:

            for j in cards_list:

                card = Card(rank=j, suit=i)

                card_list.append(card)

        return card_list

    def count_cards(self):
        """Method for counting the number of cards in a deck"""

        return len(self.cards)

    def add_card(self, card):
        """Method for adding a card to a deck"""

        self.cards.append(card)

        return

    def remove_card(self, card):
        """Method for removing a card from a deck"""

        self.cards.remove(card)

        return

    def shuffle(self):
        """Method for shuffling a deck of cards"""

        # Get the cards
        cards = self.cards

        # Shuffle
        shuffle(cards)

        # Update the deck
        self.cards = cards

        return

    def draw_card(self):
        """Method for drawing a card"""

        # If there are no cards left, return None
        if len(self.cards) == 0:

            return None

        # Get the top card from the deck
        card = self.cards[0]

        # Remove the card from the deck
        self.cards.remove(card)

        return card


if __name__ == "__main__":

    deck_test = Deck()

    deck_test.shuffle()

    card_test = deck_test.draw_card()
    card_test2 = deck_test.draw_card()

    print(card_test.unicode)
    print(card_test2.unicode)
    print(deck_test.count_cards())

    deck_test.add_card(card_test)
    print(deck_test.count_cards())

    deck_test.add_card(card_test2)
    print(deck_test.count_cards())
