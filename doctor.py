import datetime
import json
import re
from typing import Any

from common_utils import (
    convert_timedelta_to_years,
    format_date,
    format_telephone,
    generate_id,
    remove_duplicated_chars,
    validate_str_date,
)
from public_person import PublicPerson
from specialty import Specialty
from qualification import Qualification


class Doctor(PublicPerson):
    __doctor_id: int = generate_id()

    def __init__(self, *args, **kwargs) -> None:
        parsed_data: dict = Doctor.parse_init_data(*args, **kwargs)

        super().__init__(parsed_data.get('initials'), parsed_data.get('email'), parsed_data.get('public_phone'))

        self.__surname: str = Doctor.validate_name(parsed_data.get('surname'), 'surname')
        self.__firstname: str = Doctor.validate_name(parsed_data.get('firstname'), 'firstname')
        self.__patronymic: str | None = Doctor.validate_patronymic(parsed_data.get('patronymic'))
        self.__date_birth: datetime.date = Doctor.validate_date_birth(parsed_data.get('date_birth'))
        self.__private_phone: str = Doctor.validate_private_phone(parsed_data.get('private_phone'))
        self.__qualification: Qualification = Doctor.validate_qualification(parsed_data.get('qualification'))
        self.__specialties: list[Specialty] = Doctor.validate_specialties(parsed_data.get('specialties'))

    @property
    def doctor_id(self) -> int:
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
    def patronymic(self) -> str | None:
        return self.__patronymic

    @patronymic.setter
    def patronymic(self, patronymic: str | None) -> None:
        self.__patronymic = Doctor.validate_patronymic(patronymic)

    @property
    def date_birth(self) -> datetime.date:
        return self.__date_birth

    @date_birth.setter
    def date_birth(self, date_birth: datetime.date | str) -> None:
        self.__date_birth = Doctor.validate_date_birth(date_birth)

    @property
    def private_phone(self) -> str:
        return self.__private_phone

    @private_phone.setter
    def private_phone(self, private_phone: str) -> None:
        self.__private_phone = Doctor.validate_private_phone(private_phone)

    @property
    def specialties(self) -> list[Specialty]:
        return self.__specialties

    @specialties.setter
    def specialties(self, specialties: list[Specialty | str]) -> None:
        self.__specialties = Doctor.validate_specialties(specialties)

    @property
    def qualification(self) -> Qualification:
        return self.__qualification

    @qualification.setter
    def qualification(self, qualification: Qualification | str) -> None:
        self.__qualification = Doctor.validate_qualification(qualification)

    @staticmethod
    def validate_patronymic(patronymic: str | None) -> str | None:
        if patronymic is None:
            return None

        return Doctor.validate_name(patronymic, 'patronymic')

    @staticmethod
    def validate_date_birth(date_birth: datetime.date | str) -> datetime.date:
        if not isinstance(date_birth, datetime.date | str):
            raise TypeError('Дата рождения должна быть типа datetime.date или строкой')

        if isinstance(date_birth, str):
            date_birth_parts = list(map(int, validate_str_date(date_birth).split('.')))
            date_birth = datetime.date(date_birth_parts[2], date_birth_parts[1], date_birth_parts[0])

        age = convert_timedelta_to_years(datetime.date.today() - date_birth)
        if age < 18 or age > 100:
            raise ValueError('Человек должен быть старше 18 и младше 100 лет')

        return date_birth

    @staticmethod
    def validate_private_phone(private_phone: str) -> str:
        return Doctor.validate_phone(private_phone, 'личный')

    @staticmethod
    def validate_specialties(specialties: list[Specialty | str]) -> list[Specialty]:
        if not isinstance(specialties, list):
            raise TypeError('Параметр specialties должен быть списком')
        if not specialties:
            raise ValueError('Список specialties не может быть пустым')
        if any(not isinstance(specialty, Specialty | str) for specialty in specialties):
            raise TypeError('Параметр specialties должен содержать список значений типа Specialty или строк')

        return [Specialty(specialty) if isinstance(specialty, str) else specialty for specialty in specialties]

    @staticmethod
    def validate_qualification(qualification: Qualification | str) -> Qualification:
        if not isinstance(qualification, Qualification | str):
            raise TypeError('Параметр qualification должен быть типа Qualification или строкой')

        return Qualification(qualification) if isinstance(qualification, str) else qualification

    @staticmethod
    def parse_init_data(*args, **kwargs) -> dict:
        if len(args) == 1 and isinstance(args[0], Doctor):
            data = Doctor.parse_init_doctor(args[0])
        elif len(args) == 1 and isinstance(args[0], dict):
            data = Doctor.parse_init_dict(args[0])
        elif len(args) == 1 and isinstance(args[0], str):
            if args[0].startswith('{') and args[0].endswith('}'):
                data = Doctor.parse_init_json(args[0])
            else:
                data = Doctor.parse_init_string(args[0])
        elif len(args) == 9:
            data = Doctor.build_init_data(args[0], args[1], None, args[2], args[3],
                                          args[4], args[5], args[6], args[7], args[8])
        elif len(args) == 10:
            data = Doctor.build_init_data(*args)
        elif 1 < len(args) < 9 or len(args) > 10:
            raise AttributeError('Не соответствует количество аттрибутов')
        elif kwargs.get('doctor') and isinstance(kwargs.get('doctor'), Doctor):
            data = Doctor.parse_init_doctor(kwargs.get('doctor'))
        elif kwargs.get('dictionary') and isinstance(kwargs.get('dictionary'), dict):
            data = Doctor.parse_init_dict(kwargs.get('dictionary'))
        elif kwargs.get('json') and isinstance(kwargs.get('json'), dict):
            data = Doctor.parse_init_json(kwargs.get('json'))
        elif kwargs.get('string') and isinstance(kwargs.get('string'), str):
            data = Doctor.parse_init_string(kwargs.get('string'))
        else:
            data = Doctor.parse_init_dict(kwargs)

        return data

    @staticmethod
    def parse_init_doctor(doctor: "Doctor") -> dict:
        return Doctor.build_init_data(
            doctor.surname, doctor.firstname, doctor.patronymic, doctor.initials, doctor.date_birth,
            doctor.public_phone, doctor.private_phone, doctor.email,
            Qualification(doctor.qualification.title), [Specialty(specialty.title) for specialty in doctor.specialties]
        )

    @staticmethod
    def parse_init_dict(init_dict: dict) -> dict:
        if set(init_dict.keys()) - {'surname', 'firstname', 'patronymic', 'initials', 'date_birth', 'public_phone',
                                    'private_phone', 'email', 'qualification', 'specialties'}:
            raise KeyError('Переданные ключи не соответствуют')

        return init_dict

    @staticmethod
    def parse_init_string(init_string: str) -> dict:
        split_data = init_string.split(';')

        if 1 < len(split_data) < 9 or len(split_data) > 10:
            raise AttributeError('Не соответствует количество аттрибутов')

        data: list = [parameter.strip() for parameter in split_data[:-1]]
        if ',' in split_data[-1]:
            data.append(split_data[-1].strip().split(','))
        else:
            data.append([split_data[-1].strip()])

        if len(data) == 9:
            return Doctor.build_init_data(data[0], data[1], None, data[2], data[3],
                                          data[4], data[5], data[6], data[7], data[8])
        elif len(data) == 10:
            return Doctor.build_init_data(*data)

    @staticmethod
    def parse_init_json(init_json: str) -> dict:
        return json.loads(init_json)

    @staticmethod
    def build_init_data(surname: str, firstname: str, patronymic: str | None, initials: str,
                        date_birth: datetime.date | str, public_phone: str, private_phone: str, email: str,
                        qualification: Qualification | str, specialties: list[Specialty | str]) -> dict:
        return {
            'surname': surname,
            'firstname': firstname,
            'patronymic': patronymic,
            'initials': initials,
            'date_birth': date_birth,
            'public_phone': public_phone,
            'private_phone': private_phone,
            'email': email,
            'qualification': qualification,
            'specialties': specialties,
        }

    def __str__(self) -> str:
        patronymic_name = f'Отчество: {self.patronymic}\n' if self.patronymic else '\n'

        return (f'Фамилия: {self.surname}\n'
                f'Имя: {self.firstname}'
                f'{patronymic_name}'
                f'Инициалы: {self.initials}\n'
                f'Дата рождения: {format_date(self.date_birth)}\n'
                f'Публичный телефон: {format_telephone(self.public_phone)}\n'
                f'Личный телефон: {format_telephone(self.private_phone)}\n'
                f'Email: {self.email}\n'
                f'Квалификация: {self.qualification}\n'
                f'Специальности: {", ".join(map(str, self.specialties))}\n')

    @property
    def short_str(self) -> str:
        patronymic_name = f' {self.patronymic}' if self.patronymic else ''

        return f'{self.surname} {self.firstname}{patronymic_name}'

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Doctor) and self.surname == other.surname and self.firstname == other.firstname and \
               self.patronymic == other.patronymic and self.date_birth == other.date_birth and \
               self.private_phone == other.private_phone and self.qualification == other.qualification and \
               self.initials == other.initials and self.public_phone == other.public_phone and \
               self.email == other.email and all(specialty in other.specialties for specialty in self.specialties) and \
               all(specialty in self.specialties for specialty in other.specialties)
