import json
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
        self.__specialties = Doctor.validate_specialties(specialties)

    @property
    def qualification(self) -> Qualification:
        return self.__qualification

    @qualification.setter
    def qualification(self, qualification: Qualification) -> None:
        self.__qualification = Doctor.validate_qualification(qualification)

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
        elif len(args) == 4:
            data = Doctor.build_init_data(args[0], args[1], None, args[2], args[3])
        elif len(args) == 5:
            data = Doctor.build_init_data(args[0], args[1], args[2], args[3], args[4])
        elif 1 < len(args) < 4 or len(args) > 5:
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
            doctor.surname, doctor.firstname, doctor.patronymic, Qualification(doctor.qualification.title),
            [Specialty(specialty.title) for specialty in doctor.specialties]
        )

    @staticmethod
    def parse_init_dict(init_dict: dict) -> dict:
        if set(init_dict.keys()) - {'surname', 'firstname', 'patronymic', 'qualification', 'specialties'}:
            raise KeyError('Переданные ключи не соответствуют')

        return init_dict

    @staticmethod
    def parse_init_string(init_string: str) -> dict:
        splited_data = init_string.split(';')
        data = [parameter.strip() for parameter in splited_data[:-1]]
        if ',' in splited_data[-1]:
            data.append(splited_data[-1].strip().split(','))
        else:
            data.append([splited_data[-1].strip()])

        qualification, specialities = Qualification(data[-2]), [Specialty(speciality) for speciality in data[-1]]

        if len(data) == 4:
            return Doctor.build_init_data(data[0], data[1], None, qualification, specialities)
        elif len(data) == 5:
            return Doctor.build_init_data(data[0], data[1], data[2], qualification, specialities)
        else:
            raise AttributeError('В строке указано неверное количество аргументов')

    @staticmethod
    def parse_init_json(init_json: str) -> dict:
        data = json.loads(init_json)
        prepared_dict = {}
        for key in data:
            if key == 'qualification':
                if not isinstance(data[key], str):
                    raise ValueError('В JSON в поле qualification должна храниться строка с название квалификации')

                prepared_dict[key] = Qualification(data[key])
            elif key == 'specialties':
                if not isinstance(data[key], list):
                    raise ValueError('В JSON в поле specialties должен храниться список с названием специальностей')

                prepared_dict[key] = [Specialty(specialty) for specialty in data[key]]
            else:
                prepared_dict[key] = data[key]

        return Doctor.parse_init_dict(prepared_dict)

    @staticmethod
    def build_init_data(surname: str, firstname: str, patronymic: str | None,
                        qualification: Qualification, specialties: list[Specialty]) -> dict:
        return {
            'surname': surname,
            'firstname': firstname,
            'patronymic': patronymic,
            'qualification': qualification,
            'specialties': specialties,
        }

    def __str__(self):
        patronymic_name = f'Отчество: {self.patronymic}\n' if self.patronymic else '\n'

        return (f'Фамилия: {self.surname}\n'
                f'Имя: {self.firstname}'
                f'{patronymic_name}'
                f'Квалификация: {self.qualification}\n'
                f'Специальности: {", ".join(map(str, self.specialties))}\n')

    @property
    def short_str(self):
        patronymic_name = f' {self.patronymic}' if self.patronymic else ''

        return f'{self.surname} {self.firstname}{patronymic_name}'

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Doctor) and self.surname == other.surname and self.firstname == other.firstname and \
               self.patronymic == other.patronymic and self.qualification == other.qualification and \
               all(specialty in other.specialties for specialty in self.specialties) and \
               all(specialty in self.specialties for specialty in other.specialties)
