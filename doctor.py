import re
from typing import Any

from common_utils import generate_id, remove_duplicated_chars
from specialty import Specialty
from qualification import Qualification


class Doctor:
    __doctor_id: int = generate_id()

    def __init__(self, *args, **kwargs) -> None:
        parsed_data: dict = Doctor.parse_init_data(*args, **kwargs)

        self.__surname: str = Doctor.validate_name(parsed_data.get('surname'), 'surname')
        self.__firstname: str = Doctor.validate_name(parsed_data.get('firstname'), 'firstname')
        self.__patronymic: str = Doctor.validate_patronymic(parsed_data.get('patronymic'))
        self.__qualification: Qualification = Doctor.validate_qualification(parsed_data.get('qualification'))
        self.__specialties: list[Specialty] = Doctor.validate_specialties(parsed_data.get('specialties'))

    @property
    def instructor_id(self) -> int:
        return self.__doctor_id

    @property
    def surname(self) -> str:
        return self.__surname

    @surname.setter
    def surname(self, surname: str) -> None:
        self.__surname = Doctor.validate_name(surname, 'surname')

    @property
    def firstname(self) -> str:
        return self.__firstname

    @firstname.setter
    def firstname(self, firstname: str) -> None:
        self.__firstname = Doctor.validate_name(firstname, 'firstname')

    @property
    def patronymic(self) -> str:
        return self.__patronymic

    @patronymic.setter
    def patronymic(self, patronymic: str | None) -> None:
        self.__patronymic = Doctor.validate_patronymic(patronymic)

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

    @staticmethod
    def validate_name(name: str, name_type: str) -> str:
        if not isinstance(name, str):
            raise TypeError(f'Значение {name_type} должно быть строкой')

        name = remove_duplicated_chars(name.strip(" '`-"), " '`-")
        if name == '':
            raise ValueError(f'Значение {name_type} не может быть пустым')
        if re.match(r"[^а-яё'`\-\s]+", name, flags=re.IGNORECASE):
            raise ValueError(f'Значение {name_type} содержит недопустимые символы')
        if not re.match(r"^[а-яё]*(?:['`\-\s][а-яё]+)*$", name, flags=re.IGNORECASE):
            raise ValueError(f'Значение {name_type} не соответствует стандартному формату')

        separators = re.findall(r"['`\-\s]", name)
        surname_parts = list(map(lambda string: string.capitalize(), re.split(r"['`\-\s]", name)))
        name = surname_parts[0]
        for i in range(len(separators)):
            name = f'{name}{separators[i]}{surname_parts[i + 1]}'

        return name

    @staticmethod
    def validate_patronymic(patronymic: str | None) -> str | None:
        if patronymic is None:
            return None

        return Doctor.validate_name(patronymic, "patronymic")

    @staticmethod
    def validate_specialties(specialties: list[Specialty]) -> list[Specialty]:
        if not isinstance(specialties, list):
            raise TypeError('Параметр specialties должен быть списком')
        if not specialties:
            raise ValueError('Спискок specialties не может быть пустым')
        if any(not isinstance(specialty, Specialty) for specialty in specialties):
            raise TypeError('Параметр specialties должен содержать список значений типа Specialty')

        return specialties

    @staticmethod
    def validate_qualification(qualification: Qualification) -> Qualification:
        if not isinstance(qualification, Qualification):
            raise TypeError('Параметр qualification должен быть типа Qualification')

        return qualification
