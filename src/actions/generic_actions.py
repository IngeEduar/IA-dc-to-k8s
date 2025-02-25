import random

from src.data.actions.generic_actions import get_greats, get_not_found


def not_found():
    return random.choice(get_not_found())


def greet():
    return random.choice(get_greats())
