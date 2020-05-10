"""Module for playing a hand of cribbage"""

from copy import copy
from cribbage.deck import Deck, Hand


def allocate_crib(player, computer):
    """Function for allocating which player has the crib"""

    # If the player currently has the crib, give it to the computer
    if player.has_crib:

        player.take_crib()
        computer.give_crib()

    # If the computer currently has the crib, give it to the player
    elif computer.has_crib:

        computer.take_crib()
        player.give_crib()

    # Otherwise, decide who should have the crib for the first hand
    else:

        # TODO: Create function to randomly choose who gets the crib for the first hand

        pass

    return player, computer


def calculate_individual_score(player, shared_card):
    """Function for scoring an individual player's hand"""

    continue_game = True

    # Score the opponent's hand
    score = player.hand.score_hand(shared_card=shared_card)

    # Add to the opponent's total score
    player.add_to_score(score=score)

    # Check if the computer has won
    player.check_if_won()

    # If the opponent has won, end the game
    if player.has_won:

        continue_game = False

        return continue_game

    return continue_game


def calculate_crib_score(player, crib, shared_card):
    """Function for scoring an individual player's hand"""

    continue_game = True

    # Score the opponent's hand
    score = crib.score_hand(shared_card=shared_card)

    # Add to the opponent's total score
    player.add_to_score(score=score)

    # Check if the computer has won
    player.check_if_won()

    # If the opponent has won, end the game
    if player.has_won:

        continue_game = False

        return continue_game

    return continue_game


def calculate_scores(dealer, opponent, crib, shared_card):
    """Function for calculating each player's score for their hand"""

    continue_game = True

    # Score the opponent's hand
    continue_game = calculate_individual_score(player=opponent, shared_card=shared_card)

    if not continue_game:

        return continue_game

    # Then score the dealer's hand
    continue_game = calculate_individual_score(player=dealer, shared_card=shared_card)

    if not continue_game:

        return continue_game

    # Score the crib for the dealer
    continue_game = calculate_crib_score(player=dealer, crib=crib, shared_card=shared_card)

    return continue_game


def play_hand(player, computer):
    """Function for playing a hand between a player and a computer"""

    continue_game = True

    # Check that neither the player nor the computer has won
    if player.check_if_won() or computer.check_if_won():

        # If either player has won, end the game
        continue_game = False

        return continue_game

    # Create the deck for the hand, populate, and shuffle
    deck = Deck()
    deck.populate()
    deck.shuffle()

    # Create the crib
    crib = Hand(is_crib=True)

    # Give the computer a copy of all cards in the hand
    all_cards = copy(deck.cards)
    computer.add_cards_list(all_cards=all_cards)

    # Determine which player should have the crib
    player, computer = allocate_crib(player=player, computer=computer)

    # Deal to each player: the dealer is the player with the crib
    if player.has_crib:

        deck.deal(dealer_hand=player, opponent_hand=computer)

    else:

        deck.deal(dealer_hand=computer, opponent_hand=player)

    # Have each player discard into the crib
    player_discards = player.discard()
    computer_discards = computer.discard()

    # Add the discards to the crib
    for i in player_discards + computer_discards:

        crib.add_card(i)

    # Draw the shared card
    shared_card = deck.draw_card()

    # Begin pegging round
    # TODO: Create function for pegging round

    # Score the hands
    if player.has_crib:

        continue_game = calculate_scores(dealer=player, opponent=computer, crib=crib, shared_card=shared_card)

    else:

        continue_game = calculate_scores(dealer=computer, opponent=player, crib=crib, shared_card=shared_card)

    return continue_game
