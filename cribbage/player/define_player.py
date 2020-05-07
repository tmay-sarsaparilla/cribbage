"""Module for defining a player"""

from numpy import mean
from random import choice
from itertools import combinations
from cribbage.deck.define_deck import Hand
from cribbage.player.functions import prompt_player_for_input
from cribbage.deck.functions import unique_combinations


class Player:
    """Class for a player"""

    def __init__(self, player_name):

        self.name = player_name
        self.hand = Hand(is_crib=False)
        self.has_crib = False
        self.score = 0

    def has_won(self):
        """Method to check if a player has won"""

        has_won = False

        if self.score == 121:

            has_won = True

        return has_won

    def add_to_score(self, score):
        """Method to add to a player's score"""

        # Add to the score - can't be more than 121
        self.score = min(121, self.score + score)

        return

    def give_crib(self):
        """Method for giving the crib to a player"""

        self.has_crib = True

        return

    def discard(self):
        """Method for prompting a player to discard"""

        # Display the player's hand
        self.hand.display_cards()

        # Valid choices are 1 to 6
        valid_card_choices = [str(i) for i in list(range(1, 7))]

        card_choices = []
        discarded_cards = []

        # Player must select two cards
        for i in [0, 1]:

            # Have the player choose a card
            card_chosen = prompt_player_for_input(
                prompt="Choose a card to discard: ",
                valid_choices=valid_card_choices,
                invalid_selection_message="Please choose a card number between 1 and 6"
            )

            # Add to the discard list
            card_choices.append(int(card_chosen))

            # Get the card to discard
            card = self.hand.cards[int(card_chosen) - 1]

            # Add to the discarded cards
            discarded_cards.append(card)

            # Remove from valid choices list
            valid_card_choices.remove(card_chosen)

        # Confirm player's discard selections
        confirm_selection = prompt_player_for_input(
            prompt=f"Do you want to discard cards {card_choices[0]} and {card_choices[1]}? (Y/N): ",
            valid_choices=["Y", "N"],
            invalid_selection_message="Please choose Y or N"
        )

        # If not confirmed, prompt again
        if confirm_selection == "N":

            discarded_cards = self.discard()

        # Otherwise discard
        else:

            # Loop through the cards selected
            for i in discarded_cards:

                # Remove from the player's hand
                self.hand.remove_card(card=i)

        return discarded_cards


class Computer(Player):
    """Class for an Computer player"""

    def __init__(self, difficulty="standard"):

        super().__init__("Computer")
        self.difficulty = difficulty
        self.all_cards = None

    def add_cards_list(self, all_cards):
        """Method for assigning a full list of cards to the Computer player for use in decisions"""

        self.all_cards = all_cards

        return

    @staticmethod
    def calculate_combination_hand_scores(card_combinations, full_deck):
        """Method for calculating the average score of each hand combination"""

        possible_average_scores = []

        # Loop through each combination
        for i in card_combinations:

            possible_scores_list = []

            # Create a hand object
            possible_hand = Hand(is_crib=False)

            # Add each of the cards in the combination
            for card in i:

                possible_hand.add_card(card)

            # Loop through each card left in the deck
            for shared_card in full_deck:

                # Calculate the score
                possible_score = possible_hand.score_hand(shared_card=shared_card)

                # Add the score to the score list
                possible_scores_list.append(possible_score)

                # Remove the shared card from the hand
                possible_hand.remove_card(card=shared_card)

            # Calculate the mean score
            average_score = mean(possible_scores_list)

            # Add to the list
            possible_average_scores.append(average_score)

        return possible_average_scores

    def calculate_combination_crib_scores(self, card_combinations, full_deck):
        """Method for calculating the average score of each crib combination"""

        possible_average_scores = []

        # Find all combinations of the remaining cards of length 3 (two crib cards plus a shared card)
        # This list isn't deduped because the scores will change depending on which card is the shared card
        other_card_possibilities = list(combinations(full_deck, 3))

        # Loop through all hand combinations
        for i in card_combinations:

            possible_score_list = []

            # Create a crib
            possible_hand = Hand(is_crib=True)

            # Get the two discard cards and add them to the crib
            for card in [k for k in self.hand.cards if k not in i]:

                possible_hand.add_card(card)

            # Loop through the combination of other cards
            for j in other_card_possibilities:

                # Add the first two to the crib
                for card in j[0:1]:

                    possible_hand.add_card(card)

                # Calculate the score with the third card as the shared card
                possible_score = possible_hand.score_hand(shared_card=j[2])

                # Add to the list of scores
                possible_score_list.append(possible_score)

                # Remove all the cards from the hand
                for card in j:

                    possible_hand.remove_card(card)

            # Calculate the average score fro the combination
            average_score = mean(possible_score_list)

            # Append to the list
            possible_average_scores.append(average_score)

        return possible_average_scores

    def choose_combination(self, card_combinations, average_scores):
        """Method for choosing which cards to discard from a Computer's hand"""

        # Set the range of the random choice based on the computer's difficulty level
        # There will always be 15 combinations
        if self.difficulty == "easy":

            choice_range = 10

        elif self.difficulty == "standard":

            choice_range = 5

        elif self.difficulty == "hard":

            choice_range = 3

        elif self.difficulty == "perfect":

            choice_range = 1

        else:

            raise ValueError("Invalid difficulty choice")

        # Zip the combinations and scores together
        zipped_list = zip(card_combinations, average_scores)

        # Sort the list by average score
        sorted_list = sorted(zipped_list, key=lambda x: x[1], reverse=True)

        # Reduce the range of the list
        sorted_list = sorted_list[:choice_range]

        # Make a random choice of combination
        combination_choice = choice([i[0] for i in sorted_list])

        return combination_choice

    def discard(self):
        """Method to choose cards to discard"""

        # Get all cards excluding those in the computer's hand
        full_deck = [i for i in self.all_cards if i not in self.hand.cards]

        # Get all combinations of cards of length 4
        card_combinations = unique_combinations(self.hand.cards, 4, 4)

        # Check that there are 15 combinations
        if len(card_combinations) != 15:

            raise ValueError("Maths is broken: 6 choose 4 has 15 combinations")

        # Calculate the average score for each hand combination
        possible_average_hand_scores = self.calculate_combination_hand_scores(
            card_combinations=card_combinations,
            full_deck=full_deck
        )

        # Calculate the average crib score for each hand combination
        possible_average_crib_scores = self.calculate_combination_crib_scores(
            card_combinations=card_combinations,
            full_deck=full_deck
        )

        # If the computer has the crib, add crib points to hand points
        if self.has_crib:

            total_average_scores = [a + b for a, b in zip(possible_average_hand_scores, possible_average_crib_scores)]

        # If player has the crib, subtract crib points from hand points
        elif not self.has_crib:

            total_average_scores = [a - b for a, b in zip(possible_average_hand_scores, possible_average_crib_scores)]

        # Otherwise raise an error because something is broken
        else:

            raise ValueError("Attribute 'has_crib' not initialised")

        # Make a choice of combination to keep
        combination_choice = self.choose_combination(
            card_combinations=card_combinations,
            average_scores=total_average_scores
        )

        discarded_cards = []

        # Loop through cards in the computer's hand
        for i in list(self.hand.cards):  # Using a copy of the card list here as we are altering the list as we go

            # Check whether the card appears in the chosen combination
            if i not in combination_choice:

                # If not, add to the discard list
                discarded_cards.append(i)

                # Remove from the computer's hand
                self.hand.remove_card(i)

        return discarded_cards
