"""Module for functions prompting player input"""


def prompt_player_for_input(prompt, valid_choices, invalid_selection_message):
    """Function for prompting a player to select an option from a list"""

    player_choice = input(prompt).upper()

    if player_choice not in valid_choices:

        player_choice = prompt_player_for_input(prompt, valid_choices, invalid_selection_message)

    return player_choice
