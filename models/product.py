class Product:
    _id_counter = 1

    def __init__(self, name:str, purchase_price: float, selling_price: float, quantity: int):
        self._id = Product._id_counter
        Product._id_counter += 1
        self._name = name
        self.set_purchase_price(purchase_price)
        self.set_selling_price(selling_price)
        self.set_quantity(quantity)

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_purchase_price(self):
        return self._purchase_price

    def get_selling_price(self):
        return self._selling_price

    def get_quantity(self):
        return self._quantity

    def set_purchase_price(self, value: float):
        if value < 0:
            raise ValueError("Цена закупки не может быть отрицательной")
        self._purchase_price = value

    def set_selling_price(self, value: float):
        if value < 0:
            raise ValueError("Цена продажи не может быть отрицательной")
        self._selling_price = value

    def set_quantity(self, value: int):
        if value < 0:
            raise ValueError("Количество не может быть отрицательным")
        self._quantity = value