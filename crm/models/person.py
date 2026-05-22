from datetime import datetime


class Person:
    _id_counter = 1

    def __init__(self, full_name: str, phone: str, passport_data: str, date_of_birth: str):
        self._id = Person._id_counter
        Person._id_counter += 1
        self._full_name = full_name

        self.set_phone(phone)
        self.set_passport_data(passport_data)
        self.set_date_of_birth(date_of_birth)
    def get_id(self):
        return self._id

    def get_full_name(self):
        return self._full_name

    def get_phone(self):
        return self._phone

    def get_passport_data(self):
        return self._passport_data

    def get_date_of_birth(self):
        return self._date_of_birth

    def set_full_name(self, value):
        self._full_name = value

    def set_phone(self, value):
        if not value.startswith('+7') or len(value) != 12 or not value[2:].isdigit():
            raise ValueError('Ошибка. Номер телефона должен быть в формате +7XXXXXXXXXX')
        self._phone = value

    def set_passport_data(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError('Ошибка. Паспортные данные вводятся в формате: серия, номер (без пробела)')
        self._passport_data = value

    def set_date_of_birth(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError('Ошибка. Дата рождения должна быть в формате ДД.ММ.ГГГГ')
        self._date_of_birth = value

    def get_age(self) -> int:
        birth_date = datetime.strptime(self._date_of_birth, "%d.%m.%Y")
        today = datetime.now()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    def get_info(self):
        return f"{self._full_name} | Тел: {self._phone} | Паспорт: {self._passport_data} | Возраст: {self.get_age()}"

    def __str__(self):
        return self._full_name