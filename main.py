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
        initials="Иванов П.П.",
        date_birth="09.08.2004",
        public_phone="+7 (918) 328-87-27",
        private_phone="+7 (918) 328-87-72",
        email="qwe@qwe.ru",
        qualification=Qualification("Высшая категория"),
        specialties=[Specialty("Терапевт"), "Кардиолог"]
    )

    doctor = Doctor(
        surname="Петрова",
        firstname="Мария",
        initials="Петрова М.",
        date_birth="15.02.1999",
        public_phone="8 918 328-87-32",
        private_phone="8 918 328-87-72",
        email="qwe123@qwe.org",
        qualification="Первая категория",
        specialties=["Педиатр"]
    )

    doctor = Doctor("Сидоров", "Алексей", "Сидоров А.", "02.02.2000", "9928398338", "9180398338", "asd.d@asd.sad",
                    Qualification("Вторая категория"), [Specialty("Хирург")])

    doctor = Doctor("Козлов", "Дмитрий", "Владимирович", "Козлов Д.В.", datetime.date(2000, 12, 12), "89999999999",
                    "89999999999", "kozlov@gmail.com", Qualification("Высшая категория"), [Specialty("Невролог")])

    original_doctor = Doctor("Смирнова", "Анна", "Викторовна", "Смирнова А.В.", "08.08.1998", "+79999999999",
                             "+79999999999", "smirnovanna@yandex.ru",
                             Qualification("Первая категория"), [Specialty("Офтальмолог")])
    new_doctor = Doctor(doctor=original_doctor)

    data = {
        'surname': 'Федоров',
        'firstname': 'Михаил',
        'patronymic': 'Андреевич',
        'initials': 'Федоров М.А.',
        'date_birth': datetime.date(1960, 12, 12),
        'public_phone': '9999999999',
        'private_phone': '9999999999',
        'email': 'fedorov@qwe.qwe',
        'qualification': Qualification("Высшая категория"),
        'specialties': [Specialty("Уролог"), Specialty("Андролог")]
    }
    doctor = Doctor(data)

    json_data = ('{"surname": "Николаева", "firstname": "Ольга", "initials": "Николаева О.", '
                 '"date_birth": "09.08.2000", "public_phone": "9999999999", "email": "email@email.email", '
                 '"private_phone": "9999999999", "patronymic": "Игоревна", "qualification": "Первая категория", '
                 '"specialties": ["Гинеколог", "Уролог"]}')
    doctor = Doctor(json_data)

    string_data = "Кузнецов;Андрей;Кузнецов А.;09.08.2000;9999999999;9999999999;ed@qew.qe;Вторая категория;Травматолог"
    doctor = Doctor(string_data)

    string_data = "Белова;Екатерина;Павловна;Белова Е.П.;09.08.2000;89999999999;89999999999;bolova@qwe.qwe;" \
                  "Высшая категория;Эндокринолог,Диетолог"
    doctor = Doctor(string_data)

    doctor = Doctor(json='data.json')
    print(doctor)


    # 2 - тест валидации
    doctor = Doctor("Д'Арк", "Жанна", "Д'Арк Ж.", "09.08.2000", "9288328514", "89288328516", "darkjanna@gmail.com",
                    Qualification("Вторая категория"), [Specialty("Психиатр")])
    print(doctor)
    doctor = Doctor("петрова-сидорова", "Анна", "петрова-сидорова а.", "09.08.2000", "0123456789", "0123456789",
                    "petro@fjf.ir", Qualification("     Первая       категория"), [Specialty("   Терапевт      ")])
    print(doctor)
    doctor = Doctor("  ИвАнов  ", "  Петр  ", " ИваАнОв п...", "09.08.2000", "3712978827", "(371) 297-88-27",
                    "qw.12@qwe.qwe", Qualification("Высшая категория"), ["Кардиолог", Specialty("Терапевт")])
    print(doctor)

    # 3 - тест исключений
    try:
        doctor = Doctor("Ivanov", "Петр", "Ivanov П,", "09.08.2000", "9999999999", "9999999999", "asd@asd.asd",
                        Qualification("Высшая категория"), [Specialty("Терапевт")])
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        doctor = Doctor("", "Петр", "п.", "09.08.2000", "9999999999", "9999999999", "qwe@qwe.qwe",
                        Qualification("Высшая категория"), [Specialty("Терапевт")])
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        doctor = Doctor("Иванов123", "Петр", "Иванов П.", "09.08.2000", "9999999999", "9999999999", "q@w.qe",
                        Qualification("Высшая категория"), [Specialty("Терапевт")])
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        doctor = Doctor(123, "Петр", 123, "09.08.2000", "9999999999", 123, 123,
                        Qualification("Высшая категория"), [Specialty("Терапевт")])
    except TypeError as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        doctor = Doctor("Иванов", "Петр", "09.08.2000", "9999999999",
                        Qualification("Некорректная квалификация"), [Specialty("Терапевт")])
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        doctor = Doctor("Иванов", "Петр", "Иванов", "09.08.2000", "9999999999", "9999999999", "qwe@qwe.qwe",
                        Qualification("Высшая категория"), ["Терапевт"])
    except ValueError as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        doctor = Doctor("Иванов", "Петр", "Иванов П.", "09.08.2000", "9999999999", "9999999999", "qwe@qwe.qwe",
                        Qualification("Высшая категория"), [])
    except Exception as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        doctor = Doctor("Иванов", "Петр", "Иванов П.", "09.13.2000", "9999999999", "9999999999", "qwe@qwe.qwe",
                        Qualification("Высшая категория"), [])
    except Exception as e:
        print(f"Ожидаемая ошибка: {e}")

    try:
        doctor = Doctor("Иванов;Петр")
    except AttributeError as e:
        print(f"Ожидаемая ошибка: {e}")


    # 4 - прочие тесты
    print()
    doctor = Doctor("Иванов", "Петр", "Сергеевич", "иванов п.с.", "09.08.2000", "9999999999", "9999999999",
                    "ivanov@proton.kz", Qualification("Высшая категория"), [Specialty("Терапевт")])
    print(doctor.short_str)

    doctor1 = Doctor("Иванов", "Петр", "иванов п.", "09.08.2000", "9999999999", "9999999999",
                     "ivanov@proton.kz", Qualification("Высшая категория"), [Specialty("Терапевт")])
    doctor2 = Doctor("Иванов", "Петр", "иванов п.", "09.08.2000", "9999999999", "9999999999",
                     "ivanov@proton.kz", "Высшая категория", ["Терапевт"])
    print(doctor1 == doctor2)

    doctor1 = Doctor("Иванов", "Петр", "иванов п.", "09.08.2000", "9999999999", "9999999999",
                     "ivanov@proton.kz", "Высшая категория", ["Терапевт"])
    doctor2 = Doctor("Петров", "Петр", "Петров п.", "09.08.2000", "9999999999", "9999999999",
                     "ivanov@proton.kz", "Высшая категория", ["Терапевт"])
    print(doctor1 == doctor2)


if __name__ == '__main__':
    tests()
