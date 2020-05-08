"""Module for retrieving unique combinations of cards"""

from cribbage.deck.__init__ import combinations


def unique_combinations(card_list, minimum_length, maximum_length):
    """Function for retrieving unique combinations of cards of a given length"""

    # Find all combinations of cards of in specified length range
    card_combinations = [list(combinations(card_list, i)) for i in range(minimum_length, maximum_length + 1)]

    # Flatten into a single list
    card_combinations_flat = [item for sublist in card_combinations for item in sublist]

    # Deduplicate i.e (K♥, 7♦) == (7♦, K♥)
    card_combinations_deduped = []

    # Loop through every element of the list
    for i in card_combinations_flat:

        # If the set of objects in the element is already in the de-duped list, don't add
        if set(i) not in [set(j) for j in card_combinations_deduped]:
            # Otherwise, add the element
            card_combinations_deduped.append(i)

    return card_combinations_deduped
