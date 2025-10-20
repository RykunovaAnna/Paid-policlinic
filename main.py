import datetime

from doctor import Doctor
from qualification import Qualification
from specialty import Specialty


def tests():
    # 1 - тест создания
    doctor = Doctor(
        surname="Иванов",
        firstname="Парп",
        patronymic="Сергеевич",
        date_birth="09.08.2004",
        public_phone="7 (918) 328-87-27",
        private_phone="+7 (918) 328-87-72",
        email="qwe@qwe.ru",
        qualification=Qualification("Высшая категория"),
        specialties=[Specialty("Терапевт"), "Кардиолог"]
    )
    print(doctor)

    doctor = Doctor(
        surname="Петрова",
        firstname="Мария",
        date_birth="15.02.1999",
        public_phone="8 918328-87-32",
        private_phone="8 918 328-87-72",
        email="qwe123@qwe.org",
        qualification="Первая категория",
        specialties=["Педиатр"]
    )
    print(doctor)

    # Конструктор с именованными аргументами вместо позиционных
    doctor = Doctor(
        surname="Сидоров",
        firstname="Алексей",
        date_birth="02.02.2000",
        public_phone="9928398338",
        private_phone="9180398338",
        email="asd.d@asd.sad",
        qualification=Qualification("Вторая категория"),
        specialties=[Specialty("Хирург")]
    )
    print(doctor)

    doctor = Doctor(
        surname="Козлов",
        firstname="Дмитрий",
        patronymic="Владимирович",
        date_birth=datetime.date(2000, 12, 12),
        public_phone="89999999999",
        private_phone="89999999999",
        email="kozlov@gmail.com",
        qualification=Qualification("Высшая категория"),
        specialties=[Specialty("Невролог")]
    )
    print(doctor)

    # Создание через словарь
    data = {
        'surname': 'Федоров',
        'firstname': 'Михаил',
        'patronymic': 'Андреевич',
        'date_birth': datetime.date(1960, 12, 12),
        'public_phone': '9999999999',
        'private_phone': '9999999999',
        'email': 'fedorov@qwe.qwe',
        'qualification': Qualification("Высшая категория"),
        'specialties': [Specialty("Уролог"), Specialty("Андролог")]
    }
    doctor = Doctor(**data)
    print(doctor)

    # JSON строка
    json_data = ('{"surname": "Николаева", "firstname": "Ольга",  '
                 '"date_birth": "09.08.2000", "public_phone": "9999999999", "email": "email@email.email", '
                 '"private_phone": "9999999999", "patronymic": "Игоревна", "qualification": "Первая категория", '
                 '"specialties": ["Гинеколог", "Уролог"]}')
    doctor = Doctor(json_data)
    print(doctor)

    # Строка с разделителями
    string_data = "Кузнецов;Андрей;Игоревич;09.08.2000;9999999999;9999999999;ed@qew.qe;Вторая категория;Травматолог"
    doctor = Doctor(string_data)
    print(doctor)

    string_data = "Белова;Екатерина;Павловна;09.08.2000;89999999999;89999999999;bolova@qwe.qwe;" \
                  "Высшая категория;Эндокринолог,Диетолог"
    doctor = Doctor(string_data)
    print(doctor)

    # Прочие тесты
    doctor = Doctor(
        surname="Иванов",
        firstname="Петр",
        patronymic="Сергеевич",
        date_birth="09.08.2000",
        public_phone="9999999999",
        private_phone="9999999999",
        email="ivanov@proton.kz",
        qualification=Qualification("Высшая категория"),
        specialties=[Specialty("Терапевт")]
    )
    print(doctor.short_str)
    
    doctor1 = Doctor("Иванов", "Петр", "Иванович", "09.08.2000", "9999999999", "9999999999", "ivanov@proton.kz", Qualification("Высшая категория"), [Specialty("Терапевт")]) 
    doctor2 = Doctor("Иванов", "Петр", "Иванович", "09.08.2000", "9999999999", "9999999999", "ivanov@proton.kz", "Высшая категория", ["Терапевт"]) 
    print(doctor1 == doctor2) 
    doctor1 = Doctor("Иванов", "Петр", "Иванович", "09.08.2000", "9999999999", "9999999999", "ivanov@proton.kz", "Высшая категория", ["Терапевт"]) 
    doctor2 = Doctor("Петров", "Петр", "Иванович", "09.08.2000", "9999999999", "9999999999", "ivanov@proton.kz", "Высшая категория", ["Терапевт"]) 
    print(doctor1 == doctor2)


if __name__ == '__main__':
    tests()
