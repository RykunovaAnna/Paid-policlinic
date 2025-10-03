import re
from typing import Any

from common_utils import generate_id, remove_duplicated_chars


class Specialty:
    __specialty_id: int = generate_id()

    def __init__(self, title: str) -> None:
        self.__title: str = Specialty.validate_title(title)

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str) -> None:
        self.__title = Specialty.validate_title(title)

    @staticmethod
    def validate_title(title: str) -> str:
        if not isinstance(title, str):
            raise TypeError('Название специальности должно быть строкой')

        title = remove_duplicated_chars(title.strip('- '), '- ()').capitalize()
        if not title:
            raise ValueError('Название специальности не может быть пустым')
        if re.match(r'.*[^А-ЯЁа-яё\s\-()].*', title):
            raise ValueError('Название специальности содержит недопустимые символы')
        if not re.match(r'^[А-ЯЁ][а-яё]+(?:[\s\-]?[а-яё]+)+(?:\s\([а-яё]+(?:[\s\-]?[а-яё]+)*\))?$', title):
            raise ValueError('Название специальности не подходит по формату')

        return title

    def __str__(self):
        return self.title

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Specialty) and self.title == other.title
