from common_utils import generate_id


class Qualification:
    __qualification_id: int = generate_id()

    def __init__(self, title: str) -> None:
        self.__title: str = title

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str) -> None:
        self.__title = title
