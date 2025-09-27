from common_utils import generate_id
from doctor import Doctor


class PublicDoctor(Doctor):
    __public_doctor_id: int = generate_id()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.__full_fio: str = f'{self.surname} {self.firstname}.{f"{self.patronymic}." if self.patronymic else ""}'
        self.__initials: str = f'{self.surname} {self.firstname[0]}.' \
                               f'{f"{self.patronymic[0]}." if self.patronymic else ""}'

    @property
    def full_fio(self) -> str:
        return self.__full_fio

    @property
    def initials(self) -> str:
        return self.__initials
