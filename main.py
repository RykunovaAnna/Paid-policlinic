from doctor import Doctor
from qualification import Qualification
from specialty import Specialty


def tests():
    # 1 - тест создания
    doctor = Doctor(
        surname="Иванов",
        firstname="Петр",
        patronymic="Сергеевич",
        qualification=Qualification("Высшая категория"),
        specialties=[Specialty("Терапевт"), Specialty("Кардиолог")]
    )

    doctor = Doctor(
        surname="Петрова",
        firstname="Мария",
        qualification=Qualification("Первая категория"),
        specialties=[Specialty("Педиатр")]
    )

    doctor = Doctor("Сидоров", "Алексей", Qualification("Вторая категория"), [Specialty("Хирург")])

    doctor = Doctor("Козлов", "Дмитрий", "Владимирович", Qualification("Высшая категория"), [Specialty("Невролог")])

    original_doctor = Doctor("Смирнов", "Анна", "Викторовна", Qualification("Первая категория"),
                             [Specialty("Офтальмолог")])
    new_doctor = Doctor(doctor=original_doctor)

    data = {
        'surname': 'Федоров',
        'firstname': 'Михаил',
        'patronymic': 'Андреевич',
        'qualification': Qualification("Высшая категория"),
        'specialties': [Specialty("Уролог"), Specialty("Андролог")]
    }
    doctor = Doctor(data)

    json_data = '{"surname": "Николаева", "firstname": "Ольга", "patronymic": "Игоревна", "qualification": "Первая ' \
                'категория", "specialties": ["Гинеколог", "Уролог"]}'
    doctor = Doctor(json_data)

    string_data = "Кузнецов;Андрей;Вторая категория;Травматолог"
    doctor = Doctor(string_data)

    string_data = "Белова;Екатерина;Павловна;Высшая категория;Эндокринолог,Диетолог"
    doctor = Doctor(string_data)


    # 2 - тест валидации
    doctor = Doctor("Д'Арк", "Жанна", Qualification("Вторая категория"), [Specialty("Психиатр")])
    print(doctor)
    doctor = Doctor("петрова-сидорова", "Анна", Qualification("Первая категория"), [Specialty("Терапевт")])
    print(doctor)
    doctor = Doctor("  ИвАнов  ", "  Петр  ", Qualification("Высшая категория"), [Specialty("Кардиолог"), Specialty("Терапевт")])
    print(doctor)

    # 3 - тест исключений
    try:
        doctor = Doctor("Ivanov", "Петр", Qualification("Высшая категория"), [Specialty("Терапевт")])
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        doctor = Doctor("", "Петр", Qualification("Высшая категория"), [Specialty("Терапевт")])
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        doctor = Doctor("Иванов123", "Петр", Qualification("Высшая категория"), [Specialty("Терапевт")])
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        doctor = Doctor(123, "Петр", Qualification("Высшая категория"), [Specialty("Терапевт")])
    except TypeError as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        doctor = Doctor("Иванов", "Петр", Qualification("Некорректная квалификация"), [Specialty("Терапевт")])
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        doctor = Doctor("Иванов", "Петр", Qualification("Высшая категория"), ["Терапевт"])
    except TypeError as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        doctor = Doctor("Иванов", "Петр", Qualification("Высшая категория"), [])
    except Exception as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        doctor = Doctor("Иванов;Петр")  # Недостаточно параметров
    except AttributeError as e:
        print(f"Ожидаемая ошибка: {e}")


    # 4 - прочие тесты
    doctor = Doctor("Иванов", "Петр", "Сергеевич", Qualification("Высшая категория"), [Specialty("Терапевт")])
    print(doctor.short_str)  # "Иванов Петр Сергеевич"

    doctor1 = Doctor("Иванов", "Петр", Qualification("Высшая категория"), [Specialty("Терапевт")])
    doctor2 = Doctor("Иванов", "Петр", Qualification("Высшая категория"), [Specialty("Терапевт")])
    print(doctor1 == doctor2)  # Должно быть True

    doctor1 = Doctor("Иванов", "Петр", Qualification("Высшая категория"), [Specialty("Терапевт")])
    doctor2 = Doctor("Петров", "Петр", Qualification("Высшая категория"), [Specialty("Терапевт")])
    print(doctor1 == doctor2)  # Должно быть False


if __name__ == '__main__':
    tests()
