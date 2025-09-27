from typing import Any

from common_utils import generate_id, remove_duplicated_chars


class Qualification:
    __qualification_id: int = generate_id()

    def __init__(self, title: str) -> None:
        self.__title: str = Qualification.validate_title(title)

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str) -> None:
        self.__title = Qualification.validate_title(title)

    @staticmethod
    def validate_title(title: str) -> str:
        if not isinstance(title, str):
            raise TypeError('Название категории должно быть строкой')

        title = remove_duplicated_chars(title.strip(), ' ').capitalize()
        if title == '':
            raise ValueError('Категория не может быть пустой')
        if title not in ('Вторая категория', 'Первая категория', 'Высшая категория'):
            raise ValueError('Такой категории не существует')

        return title

    def __str__(self):
        return self.title

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Qualification) and self.title == other.title
