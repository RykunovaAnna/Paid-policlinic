import _io
import datetime
import json
from typing import Any

from common_utils import (
    convert_timedelta_to_years,
    format_date,
    format_telephone,
    generate_id,
    validate_str_date,
)
from public_person import PublicPerson
from specialty import Specialty
from qualification import Qualification


class Doctor(PublicPerson):
    __doctor_id: int = generate_id()

    def __init__(self, *args, **kwargs) -> None:
        parsed_data = Doctor.parse_init_data(*args, **kwargs)

        surname = Doctor.validate_name(parsed_data.get('surname'), 'surname')
        firstname = Doctor.validate_name(parsed_data.get('firstname'), 'firstname')
        patronymic = Doctor.validate_patronymic(parsed_data.get('patronymic'))
        email = PublicPerson.validate_email(parsed_data.get('email'))
        public_phone = PublicPerson.validate_public_phone(parsed_data.get('public_phone'))

        # Вызываем конструктор родителя с корректными аргументами
        super().__init__(surname, firstname, patronymic, email, public_phone)

        # Остальные поля
        self.__surname = surname
        self.__firstname = firstname
        self.__patronymic = patronymic
        self.__date_birth = Doctor.validate_date_birth(parsed_data.get('date_birth'))
        self.__private_phone = Doctor.validate_private_phone(parsed_data.get('private_phone'))
        self.__qualification = Doctor.validate_qualification(parsed_data.get('qualification'))
        self.__specialties = Doctor.validate_specialties(parsed_data.get('specialties'))

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
        if not isinstance(date_birth, (datetime.date, str)):
            raise TypeError('Дата рождения должна быть типа datetime.date или строкой')
        if isinstance(date_birth, str):
            parts = list(map(int, validate_str_date(date_birth).split('.')))
            date_birth = datetime.date(parts[2], parts[1], parts[0])
        age = convert_timedelta_to_years(datetime.date.today() - date_birth)
        if age < 18 or age > 100:
            raise ValueError('Человек должен быть старше 18 и младше 100 лет')
        return date_birth

    @staticmethod
    def validate_private_phone(phone: str) -> str:
        return Doctor.validate_phone(phone, 'личный')

    @staticmethod
    def validate_specialties(specialties: list[Specialty | str]) -> list[Specialty]:
        if not isinstance(specialties, list):
            raise TypeError('specialties должен быть списком')
        if not specialties:
            raise ValueError('Список specialties не может быть пустым')
        return [Specialty(s) if isinstance(s, str) else s for s in specialties]

    @staticmethod
    def validate_qualification(qualification: Qualification | str) -> Qualification:
        if isinstance(qualification, str):
            return Qualification(qualification)
        if isinstance(qualification, Qualification):
            return qualification
        raise TypeError('qualification должен быть Qualification или str')

    # --- Методы parse_init_data и build_init_data ---
    @staticmethod
    def parse_init_data(*args, **kwargs) -> dict:
        if len(args) == 1 and isinstance(args[0], Doctor):
            return Doctor.parse_init_doctor(args[0])
        elif len(args) == 1 and isinstance(args[0], dict):
            return args[0]
        elif len(args) == 1 and isinstance(args[0], str):
            if args[0].startswith('{') and args[0].endswith('}'):
                return json.loads(args[0])
            return Doctor.parse_init_string(args[0])
        elif len(args) in (8, 9, 10):
            return Doctor.build_init_data(*args)
        elif kwargs.get('doctor') and isinstance(kwargs.get('doctor'), Doctor):
            return Doctor.parse_init_doctor(kwargs.get('doctor'))
        elif kwargs.get('dictionary') and isinstance(kwargs.get('dictionary'), dict):
            return kwargs.get('dictionary')
        elif kwargs.get('json'):
            if isinstance(kwargs.get('json'), str):
                with open(kwargs.get('json'), 'r', encoding='utf-8') as f:
                    return json.load(f)
            elif isinstance(kwargs.get('json'), _io.TextIOWrapper):
                return json.load(kwargs.get('json'))
        elif kwargs.get('string') and isinstance(kwargs.get('string'), str):
            return Doctor.parse_init_string(kwargs.get('string'))
        else:
            return kwargs

    @staticmethod
    def parse_init_doctor(doctor: "Doctor") -> dict:
        return {
            'surname': doctor.surname,
            'firstname': doctor.firstname,
            'patronymic': doctor.patronymic,
            'initials': doctor.initials,
            'date_birth': doctor.date_birth,
            'public_phone': doctor.public_phone,
            'private_phone': doctor.private_phone,
            'email': doctor.email,
            'qualification': doctor.qualification,
            'specialties': doctor.specialties,
        }

    @staticmethod
    def parse_init_string(init_string: str) -> dict:
        split_data = init_string.split(';')
        # Простейшая проверка на корректность
        if len(split_data) < 7:
            raise AttributeError('Не соответствует количество атрибутов')
        return {
            'surname': split_data[0].strip(),
            'firstname': split_data[1].strip(),
            'patronymic': split_data[2].strip() if len(split_data) > 8 else None,
            'date_birth': split_data[3].strip(),
            'public_phone': split_data[4].strip(),
            'private_phone': split_data[5].strip(),
            'email': split_data[6].strip(),
            'qualification': split_data[7].strip() if len(split_data) > 7 else None,
            'specialties': split_data[8].strip().split(',') if len(split_data) > 8 else [],
        }

    @staticmethod
    def build_init_data(*args) -> dict:
        keys = ['surname', 'firstname', 'patronymic', 'date_birth', 'public_phone', 'private_phone', 'email', 'qualification', 'specialties']
        return dict(zip(keys, args))

    def __str__(self) -> str:
        patronymic_name = f'Отчество: {self.patronymic}\n' if self.patronymic else ''
        return (f'Фамилия: {self.surname}\n'
                f'Имя: {self.firstname}\n'
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
        if not isinstance(other, Doctor):
            return False
        return (
            self.surname == other.surname and
            self.firstname == other.firstname and
            self.patronymic == other.patronymic and
            self.date_birth == other.date_birth and
            self.private_phone == other.private_phone and
            self.qualification == other.qualification and
            self.initials == other.initials and
            self.public_phone == other.public_phone and
            self.email == other.email and
            all(s in other.specialties for s in self.specialties) and
            all(s in self.specialties for s in other.specialties)
        )
