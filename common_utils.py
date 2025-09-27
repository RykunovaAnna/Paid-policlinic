import random


def generate_id() -> int:
    return random.randint(1, 1_000_000)
