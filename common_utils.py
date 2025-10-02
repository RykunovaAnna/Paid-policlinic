import datetime
import random
import re


def generate_id() -> int:
    return random.randint(1, 1_000_000)


def remove_duplicated_chars(string: str, chars: str) -> str:
    for char in chars:
        if char in string:
            string = re.sub(re.compile(f'{char}+'), char, string)
    return string


def convert_timedelta_to_years(timedelta: datetime.timedelta) -> float:
    return timedelta.days / 365


def validate_str_date(date: str) -> str:
    if not isinstance(date, str):
        raise TypeError('Дата должна быть строкой')
    if re.match(r'[^\.\d]', date):
        raise ValueError('Дата содержит недопустимые символы')
    if not re.match(r'^\d{2}\.\d{2}\.\d+$', date):
        raise ValueError('Необходимо указывать дату в формате ДД.ММ.ГГГГ')

    date_parts = list(map(int, date.strip().split('.')))
    if any(date_part <= 0 for date_part in date_parts):
        raise ValueError('День, месяц и год должны быть целыми неотрицательными числами')
    if date_parts[1] > 12:
        raise ValueError('Месяц должен быть числом от 1 до 12')
    if date_parts[2] % 4 == 0 and date_parts[1] == 2 and date_parts[0] > 29:
        raise ValueError('В феврале високосного года существует всего 29 дней')
    if date_parts[2] % 4 != 0 and date_parts[1] == 2 and date_parts[0] > 28:
        raise ValueError('В феврале не високосного года существует всего 28 дней')
    if date_parts[1] in (1, 3, 5, 7, 8, 10, 12) and date_parts[0] > 31 or\
            date_parts[1] in (2, 4, 6, 9, 11) and date_parts[0] > 30:
        raise ValueError('Указано некорректное количество дней в месяце')

    return date


def format_telephone(telephone: str) -> str:
    return '+7 ({}) {}-{}-{}'.format(telephone[:3], telephone[3:6], telephone[6:8], telephone[8:])


def format_date(date: datetime.date) -> str:
    return '{}.{}.{}'.format(format_date_part(date.day, 'day'),
                             format_date_part(date.month, 'month'),
                             format_date_part(date.year, 'year'))


def format_date_part(date_part: int | str, date_part_name: str) -> str:
    if date_part_name in ('day', 'month'):
        return f'0{date_part}' if date_part < 10 else date_part
    elif date_part_name == 'year':
        cnt_zero = sum(map(int, [date_part < 10, date_part < 100, date_part < 1000]))
        return f"{'0' * cnt_zero}{date_part}"
