import datetime

from doctor import Doctor
from qualification import Qualification
from specialty import Specialty


def tests():
    # 1 - тест создания
    doctor = Doctor(
        surname="Иванов",
        firstname="Петр",
        patronymic="Сергеевич",
        date_birth="09.08.2004",
        private_phone="+7 (918) 328-87-72",
        qualification=Qualification("Высшая категория"),
        specialties=[Specialty("Терапевт"), "Кардиолог"]
    )

    doctor = Doctor(
        surname="Петрова",
        firstname="Мария",
        date_birth="15.02.1999",
        private_phone="8 918 328-87-72",
        qualification="Первая категория",
        specialties=["Педиатр"]
    )

    doctor = Doctor("Сидоров", "Алексей", "02.02.2000", "9180398338",
                    Qualification("Вторая категория"), [Specialty("Хирург")])

    doctor = Doctor("Козлов", "Дмитрий", "Владимирович", datetime.date(2000, 12, 12), "89999999999",
                    Qualification("Высшая категория"), [Specialty("Невролог")])

    original_doctor = Doctor("Смирнов", "Анна", "Викторовна", "08.08.1998", "+79999999999",
                             Qualification("Первая категория"), [Specialty("Офтальмолог")])
    new_doctor = Doctor(doctor=original_doctor)

    data = {
        'surname': 'Федоров',
        'firstname': 'Михаил',
        'patronymic': 'Андреевич',
        'date_birth': datetime.date(1960, 12, 12),
        'private_phone': '9999999999',
        'qualification': Qualification("Высшая категория"),
        'specialties': [Specialty("Уролог"), Specialty("Андролог")]
    }
    doctor = Doctor(data)

    json_data = ('{"surname": "Николаева", "firstname": "Ольга", "date_birth": "09.08.2000", '
                 '"private_phone": "9999999999", "patronymic": "Игоревна", "qualification": "Первая категория", '
                 '"specialties": ["Гинеколог", "Уролог"]}')
    doctor = Doctor(json_data)

    string_data = "Кузнецов;Андрей;09.08.2000;9999999999;Вторая категория;Травматолог"
    doctor = Doctor(string_data)

    string_data = "Белова;Екатерина;Павловна;09.08.2000;89999999999;Высшая категория;Эндокринолог,Диетолог"
    doctor = Doctor(string_data)


    # 2 - тест валидации
    doctor = Doctor("Д'Арк", "Жанна", "09.08.2000", "9288328514", Qualification("Вторая категория"),
                    [Specialty("Психиатр")])
    print(doctor)
    doctor = Doctor("петрова-сидорова", "Анна", "09.08.2000", "0123456789", Qualification("     Первая       категория"),
                    [Specialty("Терапевт")])
    print(doctor)
    doctor = Doctor("  ИвАнов  ", "  Петр  ", "09.08.2000", "3712978827", Qualification("Высшая категория"),
                    [Specialty("Кардиолог"), Specialty("Терапевт")])
    print(doctor)

    # 3 - тест исключений
    try:
        doctor = Doctor("Ivanov", "Петр", "09.08.2000", "9999999999", Qualification("Высшая категория"),
                        [Specialty("Терапевт")])
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        doctor = Doctor("", "Петр", "09.08.2000", "9999999999", Qualification("Высшая категория"),
                        [Specialty("Терапевт")])
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        doctor = Doctor("Иванов123", "Петр", "09.08.2000", "9999999999",
                        Qualification("Высшая категория"), [Specialty("Терапевт")])
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        doctor = Doctor(123, "Петр", "09.08.2000", "9999999999",
                        Qualification("Высшая категория"), [Specialty("Терапевт")])
    except TypeError as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        doctor = Doctor("Иванов", "Петр", "09.08.2000", "9999999999",
                        Qualification("Некорректная квалификация"), [Specialty("Терапевт")])
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        doctor = Doctor("Иванов", "Петр", "09.08.2000", "9999999999",
                        Qualification("Высшая категория"), ["Терапевт"])
    except TypeError as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        doctor = Doctor("Иванов", "Петр", "09.08.2000", "9999999999",
                        Qualification("Высшая категория"), [])
    except Exception as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        doctor = Doctor("Иванов;Петр")  # Недостаточно параметров
    except AttributeError as e:
        print(f"Ожидаемая ошибка: {e}")


    # 4 - прочие тесты
    doctor = Doctor("Иванов", "Петр", "Сергеевич", "09.08.2000", "9999999999",
                    Qualification("Высшая категория"), [Specialty("Терапевт")])
    print(doctor.short_str)

    doctor1 = Doctor("Иванов", "Петр", "09.08.2000", "9999999999",
                     Qualification("Высшая категория"), [Specialty("Терапевт")])
    doctor2 = Doctor("Иванов", "Петр", "09.08.2000", "9999999999",
                     Qualification("Высшая категория"), [Specialty("Терапевт")])
    print(doctor1 == doctor2)

    doctor1 = Doctor("Иванов", "Петр", "09.08.2000", "9999999999",
                     Qualification("Высшая категория"), [Specialty("Терапевт")])
    doctor2 = Doctor("Петров", "Петр", "09.08.2000", "9999999999",
                     Qualification("Высшая категория"), [Specialty("Терапевт")])
    print(doctor1 == doctor2)


if __name__ == '__main__':
    tests()
