from models.person import Person


class Customer(Person):

    def __init__(self, full_name: str, phone: str, passport_data: str, date_of_birth: str, sales_point_address: str):
        super().__init__(full_name, phone, passport_data, date_of_birth)
        self._sales_point_address = sales_point_address

    def get_sales_point_address(self):
        return self._sales_point_address

    def set_sales_point_address(self, value):
        self._sales_point_address = value

    def get_info(self):
        return f"Покупатель: {self.get_full_name()} | Тел: {self.get_phone()} | Пункт продажи: {self._sales_point_address}"