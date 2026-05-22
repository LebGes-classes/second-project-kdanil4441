from models.order import Order


class SalesService:
    @staticmethod
    def process_sale(sales_point, customer, cart: list, orders_list: list, products: list):
        if not sales_point.get_is_active():
            raise ValueError("Пункт продаж закрыт.")

        order = Order(customer.get_id(), sales_point.get_id(), "sale")

        for item in cart:
            pid, qty, price = item["product_id"], item["quantity"], item["price"]

            available = sales_point.get_products().get(pid, 0)
            if available < qty:
                raise ValueError(f"Недостаточно товара (ID {pid}) на точке. Доступно: {available}, нужно: {qty}")

            target_product = next((p for p in products if p.get_id() == pid), None)
            if not target_product:
                raise ValueError(f"Товар с ID {pid} не найден в каталоге.")

            sales_point.sell(pid, qty, qty * price)

            target_product.set_quantity(max(0, target_product.get_quantity() - qty))

            order.add_product(pid, qty, price)
            order.get_products()[-1]["purchase_price"] = target_product.get_purchase_price()

        orders_list.append(order)
        return order

    @staticmethod
    def process_return(sales_point, customer, cart: list, orders_list: list, products: list):
        if not sales_point.get_is_active():
            raise ValueError("Пункт продаж закрыт. Оформление возврата невозможно.")

        order = Order(customer.get_id(), sales_point.get_id(), "return")

        for item in cart:
            pid, qty, price = item["product_id"], item["quantity"], item["price"]

            product = next((p for p in products if p.get_id() == pid), None)
            if not product:
                raise ValueError(f"Товар с ID {pid} не найден в каталоге.")

            sales_point.return_product(pid, qty, qty * price)

            product.set_quantity(product.get_quantity() + qty)

            order.add_product(pid, qty, price)
            order.get_products()[-1]["purchase_price"] = product.get_purchase_price()

        orders_list.append(order)
        return order

    @staticmethod
    def process_purchase(sales_point, cart: list, orders_list: list, products: list):
        if not sales_point.get_is_active():
            raise ValueError("Пункт продаж закрыт. Закупка невозможна.")

        order = Order(0, sales_point.get_id(), "purchase")

        for item in cart:
            pid, qty, price = item["product_id"], item["quantity"], item["price"]

            product = next((p for p in products if p.get_id() == pid), None)
            if not product:
                raise ValueError(f"Товар с ID {pid} не найден в каталоге.")

            sales_point.add_product(pid, qty)

            product.set_quantity(product.get_quantity() + qty)

            order.add_product(pid, qty, price)
            order.get_products()[-1]["purchase_price"] = price

        orders_list.append(order)
        return order

    @staticmethod
    def format_receipt(order: Order) -> str:
        lines = [
            f"=== ЧЕК №{order.get_id()} ===",
            f"Дата: {order.get_date()}",
            f"Тип: {order.get_order_type().upper()}",
            f"ПП ID: {order.get_sales_point_id()}"
        ]
        if order.get_customer_id():
            lines.append(f"Клиент ID: {order.get_customer_id()}")
        lines.append("-" * 25)

        for p in order.get_products():
            lines.append(f"Товар ID {p['product_id']}: {p['quantity']} шт x {p['price']} руб")

        lines.append("-" * 25)
        lines.append(f"ИТОГО: {order.get_total_amount()} руб")
        return "\n".join(lines)

    @staticmethod
    def get_total_revenue(sales_points: list) -> float:
        return sum(sp.get_revenue() for sp in sales_points)

    @staticmethod
    def calculate_profit(orders: list, products: list) -> float:
        revenue = 0.0
        expenses = 0.0

        for order in orders:
            order_type = order.get_order_type()
            order_sum = order.get_total_amount()

            if order_type == "sale":
                revenue += order_sum
                for item in order.get_products():
                    p_price = item.get("purchase_price", 0.0)
                    expenses += item["quantity"] * p_price
            elif order_type == "return":
                revenue -= order_sum
                for item in order.get_products():
                    p_price = item.get("purchase_price", 0.0)
                    expenses -= item["quantity"] * p_price
            elif order_type == "purchase":
                expenses += order_sum

        return revenue - expenses

    @staticmethod
    def get_financial_report(sales_points: list, orders: list, products: list) -> str:
        total_revenue = SalesService.get_total_revenue(sales_points)
        net_profit = SalesService.calculate_profit(orders, products)

        return (
            "=== Финансовый отчет ===\n"
            f"Общая выручка по точкам: {total_revenue:.2f} руб.\n"
            f"Чистая прибыль (с учетом себестоимости и закупок): {net_profit:.2f} руб.\n"
            f"Всего товаров в каталоге: {sum(p.get_quantity() for p in products)} шт.\n"
            "========================"
        )