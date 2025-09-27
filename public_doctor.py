from common_utils import generate_id


class PublicDoctor:
    __public_doctor_id: int = generate_id()

    def __init__(self, initials: str, full_fio: str) -> None:
        self.__full_fio: str = full_fio
        self.__initials: str = initials

    @property
    def full_fio(self) -> str:
        return self.__full_fio

    @full_fio.setter
    def full_fio(self, full_fio: str) -> None:
        self.__full_fio = full_fio

    @property
    def initials(self) -> str:
        return self.__initials

    @initials.setter
    def initial(self, initials: str) -> None:
        self.__initials = initials
