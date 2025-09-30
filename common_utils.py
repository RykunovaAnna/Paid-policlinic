import datetime
import random
import re


def generate_id() -> int:
    return random.randint(1, 1_000_000)


def remove_duplicated_chars(string: str, chars: str) -> str:
    for char in chars:
        string = string.replace(f'{char}{char}', char)
    return string


def convert_timedelta_to_years(timedelta: datetime.timedelta) -> float:
    return timedelta.days / 365


def validate_str_date(date: str) -> str:
    if not isinstance(date, str):
        raise TypeError('Дата должна быть строкой')
    if re.match(r'[^\.\d]', date):
        raise ValueError('Дата содержит недопустимые символы')
    if not re.match(r'^\d{2}\.\d{2}\.\d{4}$', date):
        raise ValueError('Необходимо указывать дату в формате ДД.ММ.ГГГГ')

    date_parts = list(map(int, date.strip().split('.')))
    if any(date_part <= 0 for date_part in date_parts):
        raise ValueError('День, месяц и год должны быть целыми неотрицательными числами')
    if date_parts[1] > 12:
        raise ValueError('Месяц должен быть числом от 1 до 12')
    if date_parts[2] % 4 == 0 and date_parts[1] == 2 and date_parts[0] > 29:
        raise ValueError('В феврале высокосного года существует всего 29 дней')
    if date_parts[2] % 4 != 0 and date_parts[1] == 2 and date_parts[0] > 28:
        raise ValueError('В феврале не высокосного года существует всего 28 дней')
    if date_parts[1] in (1, 3, 5, 7, 8, 10, 12) and date_parts[0] > 31 or\
            date_parts[1] in (2, 4, 6, 9, 11) and date_parts[0] > 30:
        raise ValueError('Указано некорректное количество дней в месяце')

    return date


def format_telephone(telephone: str) -> str:
    return '+7 ({}) {}-{}-{}'.format(telephone[:3], telephone[3:6], telephone[6:8], telephone[8:])


def format_date(date: datetime.date) -> str:
    return '{}.{}.{}'.format(date.day, date.month, date.year)
