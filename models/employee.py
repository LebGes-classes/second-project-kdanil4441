from models.person import Person


class Employee(Person):

    def __init__(self, full_name: str, phone: str, passport_data: str, date_of_birth: str, position: str, salary: float):
        super().__init__(full_name, phone, passport_data, date_of_birth)
        self._position = position
        self.set_salary(salary)
        self._is_active = True

    def get_position(self):
        return self._position

    def get_salary(self):
        return self._salary

    def get_is_active(self):
        return self._is_active

    def set_position(self, new_position):
        self._position = new_position

    def set_salary(self, new_salary):
        if new_salary < 0:
            raise ValueError('Ошибка. Зарплата не может быть отрицательной')
        self._salary = new_salary

    def fire(self):
        self._is_active = False
        print(f"Сотрудник {self.get_full_name()} уволен.")

    def hire(self):
        self._is_active = True
        print(f"Сотрудник {self.get_full_name()} принят на работу.")

    def get_info(self):
        status = "Работает" if self._is_active else "Уволен"
        return f"Сотрудник: {self.get_full_name()}, Должность: {self._position}, ЗП: {self._salary}, Статус: {status}"