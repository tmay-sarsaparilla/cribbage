"""Module for defining a deck of cards"""

from random import shuffle
from itertools import combinations
from cribbage.card.define_card import Card, cards_list, suits_list


class Deck:
    """Class for a deck of cards"""

    def __init__(self):

        self.cards = []

    def populate(self):
        """Method for populating a deck of cards"""

        card_list = []

        for i in suits_list:

            for j in cards_list:

                card = Card(rank=j, suit=i)

                card_list.append(card)

        self.cards = card_list

        return

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

    def display_cards(self):

        sorted_cards = sorted(self.cards, key=lambda x: x.order)

        print([i.unicode for i in sorted_cards])

        return


class Hand(Deck):
    """Class for a player's hand"""

    def __init__(self, is_crib=False):

        super().__init__()
        self.is_crib = is_crib
        self.combinations = []

    def unique_card_combinations(self):
        """Method for finding all unique combinations of cards in a hand"""

        # Find all combinations of cards of lengths 1 to 5
        card_combinations = [list(combinations(self.cards, i)) for i in range(1, 6)]

        # Flatten into a single list
        card_combinations_flat = [item for sublist in card_combinations for item in sublist]

        # Deduplicate i.e (K♥, 7♦) == (7♦, K♥)
        card_combinations_deduped = []

        # Loop through every element of the list
        for i in card_combinations_flat:

            # If the set of objects in the element is already in the deduped list, don't add
            if set(i) not in [set(j) for j in card_combinations_deduped]:

                # Otherwise, add the element
                card_combinations_deduped.append(i)

        # Set the objects combinations attribute
        self.combinations = card_combinations_deduped

        return

    def count_fifteens(self):
        """Method for counting groups of cards adding up to fifteen in a hand"""

        sum_list = []

        # For each tuple in the list
        for i in self.combinations:

            # Sum the values
            combination_sum = sum([i[j].value for j in range(0, len(i))])

            # Add to the list
            sum_list.append(combination_sum)

        fifteens = sum_list.count(15)

        return fifteens

    def count_pairs(self):
        """Method for counting pairs of cards in a hand"""

        pairs = 0

        # Get the rank of each card in the hand
        card_ranks = [i.rank for i in self.cards]

        # Find the set of unique ranks in the hand
        unique_ranks = list(set(card_ranks))

        # Count how many of each rank appear in the hand
        rank_count = [card_ranks.count(i) for i in unique_ranks]

        # Loop through the counts
        for i in rank_count:

            # If 2 of a kind, add one pair
            if i == 2:

                pairs += 1

            # Three of a kind, add 3 pairs
            elif i == 3:

                pairs += 3

            # Four of a kind, add 6 pairs
            elif i == 4:

                pairs += 6

            # Otherwise continue
            else:

                continue

        return pairs

    def count_runs(self):
        """Method for counting runs of cards in a hand"""

        runs = 0

        return

    def count_nobs(self, shared_card):
        """Method for counting nobs in a hand"""

        nobs = 0

        # Get the rank and suit of the shared card
        shared_rank = shared_card.rank
        shared_suit = shared_card.suit

        # If the shared card is a Jack, player can't receive points for nob so return
        if shared_rank == "J":

            return nobs

        # Otherwise loop through the cards in the hand
        for i in self.cards:

            card_rank = i.rank
            card_suit = i.suit

            # If card is a Jack and has the same suit as the shared card, add one
            if card_rank == "J" and card_suit == shared_suit:

                nobs += 1

        return nobs

    def score_hand(self, shared_card):
        """Method for scoring a hand"""

        score = 0

        # Add shared card to hand
        self.add_card(shared_card)

        # Find all unique combinations of cards in the hand
        self.unique_card_combinations()

        # Count all fifteens (worth 2 each)
        fifteens = self.count_fifteens()

        score += fifteens * 2

        # Count all pairs (worth 2 each)
        pairs = self.count_pairs()

        score += pairs * 2

        # Count nobs
        nobs = self.count_nobs(shared_card=shared_card)

        score += nobs

        return score


if __name__ == "__main__":

    deck_test = Deck()
    deck_test.populate()

    deck_test.shuffle()

    hand_test = Hand()

    for i_test in range(0, 4):

        card_test = deck_test.draw_card()
        hand_test.add_card(card_test)

    shared_card_test = deck_test.draw_card()

    hand_test.display_cards()
    print(shared_card_test.unicode)

    score_test = hand_test.score_hand(shared_card_test)

    print(score_test)
