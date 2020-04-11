"""Module for defining a card"""


# List of face cards
ace = ["A"]
non_face_cards = [str(i) for i in range(2, 11)]
face_cards = ["J", "Q", "K"]
all_cards = ace + non_face_cards + face_cards


class Card:
    """Class for a playing card"""

    def __init__(self, rank="2", suit="S"):

        self.rank = rank,
        self.suit = suit,
        self.value = self.set_value(rank=rank)
        self.unicode = self.set_unicode(rank=rank, suit=suit)

    @staticmethod
    def set_value(rank):
        """Method for setting the value of card based on its rank"""

        # Face cards have value 10
        if rank in face_cards:

            value = 10

        # Aces have value 1
        elif rank in ace:

            value = 1

        # All other cards have the same value as their rank
        elif rank in non_face_cards:

            value = int(rank)

        else:

            raise ValueError("Invalid rank")

        return value

    @staticmethod
    def set_unicode(rank, suit):
        """Method for setting the unicode representation of a card"""

        suit_unicode_characters = {

            "S": u"\u2660",
            "H": u"\u2665",
            "D": u"\u2666",
            "C": u"\u2663"

        }

        try:

            suit_unicode = suit_unicode_characters[suit]

        except KeyError:

            raise ValueError("Invalid suit")

        unicode = rank + suit_unicode

        return unicode

    def display_card(self):
        """Method for displaying a card"""

        print("|" + self.unicode + "|")


if __name__ == "__main__":

    print(face_cards)
    print(ace)
    print(non_face_cards)

    test_card = Card("2", "H")

    test_card.display_card()
