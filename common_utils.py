import random


def generate_id() -> int:
    return random.randint(1, 1_000_000)


def remove_duplicated_chars(string: str, chars: str) -> str:
    for char in chars:
        string = string.replace(f'{char}{char}', char)
    return string
