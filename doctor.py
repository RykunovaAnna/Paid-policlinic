from common_utils import generate_id
from specialty import Specialty
from qualification import Qualification


class Doctor:
    __doctor_id: int = generate_id()

    def __init__(self, surname: str, firstname: str, qualification: Qualification,
                 specialties: list[Specialty], patronymic: str | None = None) -> None:
        self.__surname: str = surname
        self.__firstname: str = firstname
        self.__patronymic: str = patronymic
        self.__qualification: Qualification = qualification
        self.__specialties: list[Specialty] = specialties

    @property
    def instructor_id(self) -> int:
        return self.__doctor_id

    @property
    def surname(self) -> str:
        return self.__surname

    @surname.setter
    def surname(self, surname: str) -> None:
        self.__surname = surname

    @property
    def firstname(self) -> str:
        return self.__firstname

    @firstname.setter
    def firstname(self, firstname: str) -> None:
        self.__firstname = firstname

    @property
    def patronymic(self) -> str:
        return self.__patronymic

    @patronymic.setter
    def patronymic(self, patronymic: str | None) -> None:
        self.__patronymic = patronymic

    @property
    def specialties(self) -> list[Specialty]:
        return self.__specialties

    @specialties.setter
    def specialties(self, specialties: list[Specialty]) -> None:
        self.__specialties = specialties

    @property
    def qualification(self) -> Qualification:
        return self.__qualification

    @qualification.setter
    def qualification(self, qualification: Qualification) -> None:
        self.__qualification = qualification
