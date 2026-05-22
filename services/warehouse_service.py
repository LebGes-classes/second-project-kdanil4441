class WarehouseService:

    @staticmethod
    def search_product(warehouse, product_id: int):
        found_items = []
        for cell in warehouse.get_cells():
            products = cell.get_products()
            if product_id in products:
                found_items.append({
                    "cell_id": cell.get_id(),
                    "cell_number": cell.get_cell_number(),
                    "quantity": products[product_id]
                })
        return found_items

    @staticmethod
    def move_product(warehouse, product_id: int, quantity: int, from_cell_id: int, to_cell_id: int):
        if from_cell_id == to_cell_id:
            raise ValueError("Нельзя переместить товар в ту же ячейку.")
        warehouse.move_product(product_id, quantity, from_cell_id, to_cell_id)
        return True

    @staticmethod
    def add_stock(warehouse, cell_id: int, product_id: int, quantity: int, products: list):
        cell = warehouse.get_cell_by_id(cell_id)
        if not cell:
            raise ValueError("Ячейка с таким ID не найдена на этом складе.")

        target_product = next((p for p in products if p.get_id() == product_id), None)
        if not target_product:
            raise ValueError(f"Товар с ID {product_id} не существует. Сначала добавьте товар в каталог.")

        cell.add_product(product_id, quantity)
        target_product.set_quantity(target_product.get_quantity() - quantity)

    @staticmethod
    def remove_stock(warehouse, cell_id: int, product_id: int, quantity: int, products: list):
        cell = warehouse.get_cell_by_id(cell_id)
        if not cell:
            raise ValueError("Ячейка с таким ID не найдена на этом складе.")

        cell.remove_product(product_id, quantity)

        target_product = next((p for p in products if p.get_id() == product_id), None)
        if target_product:
            new_qty = max(0, target_product.get_quantity() - quantity)
            target_product.set_quantity(new_qty)

    @staticmethod
    def get_full_stock_report(warehouse):
        lines = [f"Отчет по складу: {warehouse.get_name()}"]
        lines.append("=" * 40)

        cells = warehouse.get_cells()
        if not cells:
            lines.append("Склад пустой (нет ячеек)")
            return "\n".join(lines)

        for cell in cells:
            products = cell.get_products()
            if products:
                lines.append(f"Ячейка {cell.get_cell_number()} (ID: {cell.get_id()}):")
                for pid, qty in products.items():
                    lines.append(f"   - Товар ID {pid}: {qty} шт.")
            else:
                lines.append(f"Ячейка {cell.get_cell_number()} (ID: {cell.get_id()}): Пусто")

        return "\n".join(lines)