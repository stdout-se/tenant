import random


def from_dungeon_level(table, dungeon_level: int):
    for (value, level) in reversed(table):
        if dungeon_level >= level:
            return value

    return 0


def random_choice_from_dict(choice_dict: dict):
    """
    Provided a dictionary, will return a randomly selected key string. The key is randomly selected based on relative
    weights, provided for each key as a value.

    Example:
    dict = {'orc': 80, 'troll': 30, 'demon': 5}
    random_choice_from_dict(dict)

    This will return a choice of either 'orc', 'troll' or 'demon' according to the relative weights provided.

    :param choice_dict: Dictionary, where keys are options and values are their relative weights
    :return: Random choice, selected according to provided weights
    """

    population = list(choice_dict.keys())  # Ex: ['orc', 'troll', 'demon']
    relative_weights = list(choice_dict.values())  # Ex: [80, 30, 5]

    return random.choices(population, weights=relative_weights)[0]  # Take item from list with a single item
