from models.warehouse_cell import WarehouseCell

class Warehouse:
    _id_counter = 1

    def __init__(self, name: str, address: str, responsible_person_id: int = None):
        self._id = Warehouse._id_counter
        Warehouse._id_counter += 1

        self._name = name
        self._address = address
        self._responsible_person_id = responsible_person_id
        self._cells = []
        self._is_active = True

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_address(self):
        return self._address

    def get_responsible_person_id(self):
        return self._responsible_person_id

    def get_cells(self):
        return self._cells

    def get_is_active(self):
        return self._is_active

    def set_name(self, value: str):
        self._name = value

    def set_address(self, value: str):
        self._address = value

    def set_responsible_person_id(self, value: int):
        self._responsible_person_id = value

    def set_is_active(self, value: bool):
        self._is_active = value

    def add_cell(self, cell_number: str):
        new_cell = WarehouseCell(self._id, cell_number)
        self._cells.append(new_cell)
        return new_cell

    def remove_cell(self, cell_id: int):
        self._cells = [c for c in self._cells if c.get_id() != cell_id]

    def change_responsible(self, employee_id: int):
        self._responsible_person_id = employee_id

    def get_cell_by_id(self, cell_id: int):
        for cell in self._cells:
            if cell.get_id() == cell_id:
                return cell
        return None

    def move_product(self, product_id: int, quantity: int, from_cell_id: int, to_cell_id: int):
        src = self.get_cell_by_id(from_cell_id)
        dst = self.get_cell_by_id(to_cell_id)
        if not src or not dst:
            raise ValueError("Ячейка не найдена")
        src.remove_product(product_id, quantity)
        dst.add_product(product_id, quantity)

    def get_info(self) -> str:
        status = "Активен" if self._is_active else "Заблокирован"
        resp = f"ID сотрудника {self._responsible_person_id}" if self._responsible_person_id else "Нет"
        return f"Склад: {self._name} | Адрес: {self._address} | Ответственный: {resp} | Статус: {status}"