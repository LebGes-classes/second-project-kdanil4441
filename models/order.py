from datetime import datetime

class Order:
    _id_counter = 1

    def __init__(self, customer_id: int, sales_point_id: int, order_type: str = "sale"):
        self._id = Order._id_counter
        Order._id_counter += 1
        self._customer_id = customer_id
        self._sales_point_id = sales_point_id
        self._products = []
        self._date = datetime.now().strftime("%d.%m.%Y %H:%M")
        self._order_type = order_type

    def get_id(self):
        return self._id

    def get_customer_id(self):
        return self._customer_id

    def get_sales_point_id(self):
        return self._sales_point_id

    def get_products(self):
        return self._products

    def get_date(self):
        return self._date

    def get_order_type(self):
        return self._order_type

    def set_customer_id(self, value: int):
        self._customer_id = value

    def set_sales_point_id(self, value: int):
        self._sales_point_id = value

    def set_order_type(self, value: str):
        if value not in ["sale", "return", "purchase"]:
            raise ValueError("Неверный тип заказа")
        self._order_type = value

    def add_product(self, product_id: int, quantity: int, price: float, purchase_price: float = 0.0):
        if quantity <= 0 or price < 0:
            raise ValueError("Количество или цена не могут быть отрицательными")
        self._products.append({
            "product_id": product_id,
            "quantity": quantity,
            "price": price,
            "purchase_price": purchase_price
        })

    def get_total_amount(self) -> float:
        total = 0
        for item in self._products:
            total += item["quantity"] * item["price"]
        return total

    def get_info(self) -> str:
        return f"Заказ #{self._id} | Тип: {self._order_type} | Клиент: {self._customer_id} | Пункт: {self._sales_point_id} | Сумма: {self.get_total_amount()}₽"