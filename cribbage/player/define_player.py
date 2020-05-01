"""Module for defining a player"""

from cribbage.deck.define_deck import Hand, Deck
from cribbage.player.functions import prompt_player_for_input


class Player:
    """Class for a player"""

    def __init__(self, player_name):

        self.name = player_name
        self.hand = Hand(is_crib=False)
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

    def __init__(self, difficulty):

        super().__init__("Computer")
        self.difficulty = difficulty
        self.master_deck = None

    def set_master_deck(self, master_deck):
        """Method for setting the full deck for the computer player"""

        self.master_deck = master_deck

        return

    def discard(self):
        """Method to choose cards to discard"""

        # Get all cards excluding those in the computer's hand
        master_deck = [i for i in self.master_deck.cards if i not in self.hand.cards]

        print(len(master_deck))

        # Get all combinations of cards of length 4
        self.hand.unique_card_combinations()
        combinations = [i for i in self.hand.combinations if len(i) == 4]

        possible_scores_list = []

        for i in combinations:

            possible_hand = Hand(is_crib=False)

            for card in i:

                possible_hand.add_card(card)

            for shared_card in master_deck:

                possible_score = possible_hand.score_hand(shared_card=shared_card)

                possible_scores_list.append(possible_score)

        print(possible_scores_list)

        return
