import re

from common_utils import generate_id, remove_duplicated_chars


class PublicPerson:
    __public_person_id: int = generate_id()

    def __init__(self, initials: str, email: str, public_phone: str) -> None:
        self.__initials: str = PublicPerson.validate_initials(initials)
        self.__email: str = PublicPerson.validate_email(email)
        self.__public_phone: str = PublicPerson.validate_public_phone(public_phone)

    @property
    def public_person_id(self) -> int:
        return self.__public_person_id

    @property
    def initials(self) -> str:
        return self.__initials

    @initials.setter
    def initials(self, initials: str) -> None:
        self.__initials = PublicPerson.validate_initials(initials)

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email: str) -> None:
        self.__email = PublicPerson.validate_email(email)

    @property
    def public_phone(self) -> str:
        return self.__public_phone

    @public_phone.setter
    def public_phone(self, public_phone: str) -> None:
        self.__public_phone = PublicPerson.validate_public_phone(public_phone)

    @staticmethod
    def validate_initials(initials: str) -> str:
        if not isinstance(initials, str):
            raise TypeError('Фамилия и инициалы должны быть строкой')

        initials = remove_duplicated_chars(initials.strip(" '`-"), " '`-.")
        if not initials:
            raise ValueError('Фамилия и инициалы не могут быть пустой строкой')

        initials_parts = initials.split()
        if len(initials_parts) != 2:
            raise ValueError('Фамилия и инициалы должны быть разделены одним пробелом')
        if re.match(r'[^а-яё\'`\-\s\.]', initials, flags=re.IGNORECASE):
            raise ValueError('Фамилия и инициалы содержат недопустимые символы')
        if not re.match(r'^[а-яё]+(?:[\'`\-\s][а-яё]+)*$', initials_parts[0], flags=re.IGNORECASE):
            raise ValueError('Фамилия не соответствует стандартному виду')
        if not re.match(r'^(?:[а-яё]\.(?:[\-\s][а-яё]\.)*|[а-яё](?:[\'`][а-яё]\.))+$',
                        initials_parts[1], flags=re.IGNORECASE):
            raise ValueError('Инициалы не соответствуют стандартному виду')

        return f'{initials_parts[0].capitalize()} {initials_parts[1].upper()}'

    @staticmethod
    def validate_email(email: str) -> str:
        if not isinstance(email, str):
            raise TypeError('Email должен быть строкой')
        if not email:
            raise ValueError('Email не должен быть пустым')

        email_parts = email.split('@')
        if len(email_parts) != 2:
            raise ValueError('Email должен содержать только один символ "@"')
        if any(email_part.startswith('.') or email_part.startswith('-') for email_part in email_parts):
            raise ValueError('Локальная часть и доменное имя email не могут начинаться с ".", "-"')
        if any(email_part.endswith('.') or email_part.endswith('-') for email_part in email_parts):
            raise ValueError('Локальная часть и доменное имя email не могут заканчиваться ".", "-"')
        if any('..' in email_part or '--' in email_part for email_part in email_parts):
            raise ValueError('Локальная часть и доменное имя email не могут содержать подряд идущие ".", "-"')
        if '-.' in email_parts[1]:
            raise ValueError('Доменная метка не может заканчиваться на "-"')
        if re.match(r'[^a-z\d!#$%&\'*+/=?^_`{|}~\-.]', email_parts[0], flags=re.IGNORECASE):
            raise ValueError('Локальная часть email содержит недопустимые символы')
        if not re.match(r'^[a-z\d!#$%&\'*+/=?^_`{|}~\-]+(?:\.[a-z\d!#$%&\'*+/=?^_`{|}~\-]+)*$',
                        email_parts[0], flags=re.IGNORECASE):
            raise ValueError('Локальная часть email не соответствует стандартному виду')
        if re.match(r'[^a-z\d\-.]', email_parts[1], flags=re.IGNORECASE):
            raise ValueError('Доменное имя email содержит недопустимые символы')
        if not re.match(r'^[a-z\d]+(?:\-[a-z\d]+)*(?:\.[a-z\d]+(?:\-[a-z\d]+)*)\.[a-z]{2,}$',
                        email_parts[1], flags=re.IGNORECASE):
            raise ValueError('Доменное имя email не соответствует стандартному виду')

        return email

    @staticmethod
    def validate_public_phone(public_phone: str) -> str:
        if not isinstance(public_phone, str):
            raise TypeError('Публичный телефон должен быть строкой')

        public_phone = re.sub(r'[+()\s\-]', '', public_phone)
        if not public_phone:
            raise ValueError('Публичный телефон не может быть пустым')
        if re.match(r'\D', public_phone):
            raise ValueError('Публичный телефон содержит недопустимые символы')
        if not re.match(r'^(?:7\d{10}|8\d{10}|\d{10})$', public_phone):
            raise ValueError('Публичный телефон не соответствует стандартному виду')

        return public_phone if len(public_phone) == 10 else public_phone[1:]
