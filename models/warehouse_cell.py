class WarehouseCell:
    _id_counter = 1

    def __init__(self, warehouse_id: int, cell_number: str):
        self._id = WarehouseCell._id_counter
        WarehouseCell._id_counter += 1
        self._warehouse_id = warehouse_id
        self._cell_number = cell_number
        self._products = {}

    def get_id(self):
        return self._id

    def get_warehouse_id(self):
        return self._warehouse_id

    def get_cell_number(self):
        return self._cell_number

    def get_products(self):
        return self._products

    def set_cell_number(self, value: str):
        self._cell_number = value

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
            raise ValueError("Недостаточно товара в ячейке")
        self._products[product_id] = current - quantity
        if self._products[product_id] == 0:
            del self._products[product_id]

    def get_info(self) -> str:
        return f"Ячейка: {self._cell_number} | Склад ID: {self._warehouse_id} | Позиций: {len(self._products)}"