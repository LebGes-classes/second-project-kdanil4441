class SalesPoint:
    _id_counter = 1

    def __init__(self, name:str, address: str, responsible_person_id: int = None):
        self._id = SalesPoint._id_counter
        SalesPoint._id_counter += 1
        self._name = name
        self._address = address
        self._responsible_person_id = responsible_person_id
        self._products ={}
        self._is_active = True
        self._revenue = 0.0

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_address(self):
        return self._address

    def get_responsible_person_id(self):
        return self._responsible_person_id

    def get_products(self):
        return self._products

    def get_is_active(self):
        return self._is_active

    def get_revenue(self):
        return self._revenue

    def set_name(self, value: str):
        self._name = value

    def set_address(self, value: str):
        self._address = value

    def set_responsible_person_id(self, value: int):
        self._responsible_person_id = value

    def set_is_active(self, value: bool):
        self._is_active = value

    def open(self):
        self._is_active = True
        print(f"Пункт продаж {self._name} открыт.")

    def close(self):
        self._is_active = False
        print(f"Пункт продаж {self._name} закрыт.")

    def change_responsible(self, employee_id: int):
        self._responsible_person_id = employee_id

    def add_product(self, product_id: int, quantity: int):
        if quantity <= 0:
            raise ValueError('Количество должно быть положительным')
        current = self._products.get(product_id, 0)
        self._products[product_id] = current + quantity

    def remove_product(self, product_id: int, quantity: int):
        if quantity <= 0:
            raise ValueError('Количество должно быть положительным')
        current = self._products.get(product_id, 0)
        if current < quantity:
            raise ValueError('Недостаточно товара в пункте продаж')
        self._products[product_id] = current - quantity
        if self._products[product_id] == 0:
            del self._products[product_id]

    def sell(self, product_id: int, quantity: int, total_price: float):
        if total_price <= 0:
            raise ValueError('Сумма продажи должна быть положительной')
        self.remove_product(product_id, quantity)
        self._revenue += total_price

    def return_product(self, product_id: int, quantity: int, refund_amount: float):
        if refund_amount <= 0:
            raise ValueError("Сумма возврата должна быть положительной")
        self.add_product(product_id, quantity)
        self._revenue -= refund_amount

    def get_info(self) -> str:
        status = "Открыт" if self._is_active else "Закрыт"
        return f"ID: {self._id} | Пункт: {self._name} | Адрес: {self._address} | Ответственный ID: {self._responsible_person_id} | Статус: {status} | Выручка: {self._revenue}₽"