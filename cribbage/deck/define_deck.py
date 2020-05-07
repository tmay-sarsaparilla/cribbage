"""Module for defining a deck of cards"""

from random import shuffle
from operator import itemgetter
from itertools import combinations, groupby
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

    def sort_cards(self):
        """Method for sorting a deck by the order and suit of its cards"""

        # Sort the cards
        self.cards.sort(key=lambda x: x.order)

        return

    def display_cards(self):
        """Method for displaying a deck of cards"""

        # Sort cards in the deck
        self.sort_cards()

        # Print the cards
        unicode_list = [i.unicode for i in self.cards]

        print_output = ""

        print_output += "\t".join(unicode_list)

        card_numbers = "\t".join([str(i) for i in list(range(1, len(unicode_list) + 1))])

        print_output += f"\n{card_numbers}"

        print(print_output)

        return

    def deal(self, dealer_hand, opponent_hand):
        """Method for dealing cards to players' hands"""

        # Deal six cards to each player
        for i in range(0, 6):

            # Deal to opponent first
            opponent_hand.add_card(self.draw_card())

            # Then to dealer
            dealer_hand.add_card(self.draw_card())

        return dealer_hand, opponent_hand


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

        runs_of_three = 0
        runs_of_four = 0
        runs_of_five = 0

        # Get the card orders
        card_orders = [i.order for i in self.cards]

        # Get the unique set of card orders
        card_order_set = list(set(card_orders))

        # Order the set
        card_order_set.sort()

        runs_list = []

        # Group the set into runs of consecutive numbers
        # This is done by grouping by the index of the number minus its value
        # E.g. 1, 2 becomes 1-1=0, 2-2=0 and therefore group together
        for k, g in groupby(enumerate(card_order_set), lambda x: x[0] - x[1]):

            group = (map(itemgetter(1), g))
            group_list = list(map(int, group))
            runs_list.append(group_list)

        # Calculate the length of each run found
        run_length_list = [len(i) for i in runs_list]

        # If there are no runs greater than length 2, return
        if len(runs_list) == 0 or max(run_length_list) <= 2:

            return runs_of_three, runs_of_four, runs_of_five

        # Only retain runs greater than 2 in length
        runs_list_redux = [i for i in runs_list if len(i) > 2]

        # At this point there should only be one run left
        try:

            run = runs_list_redux[0]

        # If not, something has gone wrong
        except IndexError:

            raise IndexError("More than one run of cards left after reduction")

        # There's at least one run
        runs_count = 1

        # Look for duplicate orders in the full list
        # i.e. 4, 4, 5, 6 means there are two runs of length three
        for i in run:

            # If there are duplicates, apply a multiplier to the count
            order_count = card_orders.count(i)
            runs_count *= order_count

        # Determine length of the run
        run_length = len(run)

        # Increase the relevant counts
        if run_length == 3:

            runs_of_three += runs_count

        elif run_length == 4:

            runs_of_four += runs_count

        elif run_length == 5:

            runs_of_five += runs_count

        else:

            raise ValueError("Invalid run length")

        return runs_of_three, runs_of_four, runs_of_five

    def count_flushes(self, shared_card):
        """Method for counting flushes in a hand"""

        four_card_flush = 0
        five_card_flush = 0

        # Get the suits of all cards excluding the shared card
        hand_suits = [i.suit for i in self.cards if i != shared_card]

        # Get the unique set of suits
        suits_set = list(set(hand_suits))

        # If there is only one suit in the hand
        if len(suits_set) == 1:

            # If the shared card has the same suit, it's a five card flush
            if shared_card.suit in suits_set:

                five_card_flush += 1

            # Otherwise it's a four card flush
            else:

                # Crib hand can only score on a five card flush
                if not self.is_crib:

                    four_card_flush += 1

        return four_card_flush, five_card_flush

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

        # Count runs of cards
        runs_of_three, runs_of_four, runs_of_five = self.count_runs()

        score += runs_of_three * 3 + runs_of_four * 4 + runs_of_five * 5

        # Count flushes
        four_card_flush, five_card_flush = self.count_flushes(shared_card=shared_card)

        score += four_card_flush * 4 + five_card_flush * 5

        # Count nobs
        nobs = self.count_nobs(shared_card=shared_card)

        score += nobs

        return score


if __name__ == "__main__":

    cards_test = [Card("A", "H"), Card("A", "S"), Card("7", "H"), Card("7", "D")]

    shared_card_test = Card("4", "C")

    hand_test = Hand(is_crib=False)

    for i_test in cards_test:

        hand_test.add_card(i_test)

    hand_test.display_cards()
    print(shared_card_test.unicode)
    score_test = hand_test.score_hand(shared_card_test)

    print(score_test)
