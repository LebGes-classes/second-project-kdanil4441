import sys
from datetime import datetime
from storage.file_handler import FileHandler
from services.employee_service import EmployeeService
from services.customer_service import CustomerService
from services.sales_service import SalesService
from services.warehouse_service import WarehouseService
from models.product import Product
from models.warehouse import Warehouse
from models.sales_point import SalesPoint


def main():
    handler = FileHandler()
    employees, customers, products, warehouses, sales_points, orders = handler.load_all()

    while True:
        print("\n=== ГЛАВНОЕ МЕНЮ ===")
        print("1. Сотрудники")
        print("2. Клиенты")
        print("3. Товары")
        print("4. Склады")
        print("5. Пункты продаж")
        print("6. Операции (Продажа/Закупка/Возврат)")
        print("7. Финансовый отчет")
        print("8. Выход (с сохранением)")

        choice = input("Выбор (1-8): ").strip()

        try:
            if choice == "1":
                manage_employees(employees, warehouses, sales_points)
            elif choice == "2":
                manage_customers(customers)
            elif choice == "3":
                manage_products(products)
            elif choice == "4":
                manage_warehouses(warehouses, products)
            elif choice == "5":
                manage_sales_points(sales_points, employees)
            elif choice == "6":
                manage_sales(sales_points, customers, orders, products)
            elif choice == "7":
                print("\n" + SalesService.get_financial_report(sales_points, orders, products))
            elif choice == "8":
                handler.save_all(employees, customers, products, warehouses, sales_points, orders)
                print("Данные успешно сохранены. Пока!")
                sys.exit(0)
            else:
                print("Неверный пункт меню.")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")


def manage_employees(employees, warehouses, sales_points):
    print("\n--- Сотрудники ---")
    print("1. Нанять | 2. Уволить | 3. На склад | 4. На пункт | 5. Список")
    sub = input("Выбор: ").strip()

    if sub == "1":
        # 1. ФИО
        f_name = input("ФИО: ").strip()
        if not f_name:
            print("Ошибка: ФИО не может быть пустым")
            return

        phone = input("Телефон (+7XXXXXXXXXX): ").strip()
        if not phone.startswith('+7') or len(phone) != 12 or not phone[2:].isdigit():
            print("Ошибка: Телефон должен быть в формате +7XXXXXXXXXX")
            return

        passport = input("Паспорт (10 цифр): ").strip()
        if len(passport) != 10 or not passport.isdigit():
            print("Ошибка: Паспорт должен содержать 10 цифр")
            return

        dob = input("Дата рождения (ДД.ММ.ГГГГ): ").strip()
        try:
            datetime.strptime(dob, '%d.%m.%Y')
        except ValueError:
            print("Ошибка: Дата должна быть в формате ДД.ММ.ГГГГ")
            return

        # 5. Должность
        pos = input("Должность: ").strip()
        if not pos:
            print("Ошибка: Должность не может быть пустой")
            return

        sal_str = input("Зарплата (число): ").strip()
        try:
            sal = float(sal_str)
            if sal < 0:
                print("Ошибка: Зарплата не может быть отрицательной")
                return
        except ValueError:
            print("Ошибка: Зарплата должна быть числом")
            return

        try:
            EmployeeService.hire(employees, f_name, phone, passport, dob, pos, sal)
            print("Сотрудник успешно нанят.")
        except ValueError as e:
            print("Ошибка при найме: " + str(e))

    elif sub == "2":
        try:
            eid = int(input("ID сотрудника для увольнения: "))
            emp = next((e for e in employees if e.get_id() == eid), None)
            if emp:
                EmployeeService.fire(emp)
            else:
                print("Сотрудник не найден.")
        except ValueError:
            print("Ошибка: ID должен быть числом.")

    elif sub == "3":
        try:
            wid = int(input("ID склада: "))
            eid = int(input("ID сотрудника: "))
            wh = next((w for w in warehouses if w.get_id() == wid), None)
            emp = next((e for e in employees if e.get_id() == eid), None)
            if wh and emp:
                EmployeeService.set_warehouse_responsible(wh, emp)
                print("Ответственный назначен.")
            else:
                print("Склад или сотрудник не найдены.")
        except ValueError:
            print("Ошибка: ID должен быть числом.")

    elif sub == "4":
        try:
            sid = int(input("ID пункта продаж: "))
            eid = int(input("ID сотрудника: "))
            sp = next((s for s in sales_points if s.get_id() == sid), None)
            emp = next((e for e in employees if e.get_id() == eid), None)
            if sp and emp:
                EmployeeService.set_sales_point_responsible(sp, emp)
                print("Ответственный назначен.")
            else:
                print("Пункт или сотрудник не найдены.")
        except ValueError:
            print("Ошибка: ID должен быть числом.")

    elif sub == "5":
        if not employees:
            print("Список сотрудников пуст.")
        else:
            print("\n=== Список сотрудников ===")
            for emp in employees:
                print(emp.get_info())
            print("========================")


def manage_customers(customers):
    print("\n--- Клиенты ---")
    print("1. Добавить | 2. Список")
    sub = input("Выбор: ").strip()

    if sub == "1":
        f_name = input("ФИО: ").strip()
        if not f_name: print("Ошибка: Пустое поле"); return

        phone = input("Телефон (+7XXXXXXXXXX): ").strip()
        if not phone.startswith('+7') or len(phone) != 12 or not phone[2:].isdigit():
            print("Ошибка: Неверный формат телефона"); return

        passport = input("Паспорт (10 цифр): ").strip()
        if len(passport) != 10 or not passport.isdigit():
            print("Ошибка: Паспорт должен быть 10 цифр"); return

        dob = input("Дата рождения (ДД.ММ.ГГГГ): ").strip()
        try: datetime.strptime(dob, '%d.%m.%Y')
        except ValueError: print("Ошибка: Неверный формат даты"); return

        addr = input("Адрес пункта продаж: ").strip()

        try:
            CustomerService.add_customer(customers, f_name, phone, passport, dob, addr)
            print("Клиент добавлен.")
        except ValueError as e: print("Ошибка: " + str(e))

    elif sub == "2":
        for c in customers: print(c.get_info())


def manage_products(products):
    print("\n--- Товары ---")
    print("1. Добавить | 2. Список")
    sub = input("Выбор: ").strip()

    if sub == "1":
        name = input("Название: ").strip()
        if not name: print("Ошибка: Пустое название"); return

        buy_str = input("Цена закупки: ").strip()
        sell_str = input("Цена продажи: ").strip()
        qty_str = input("Количество: ").strip()

        try:
            if not buy_str.replace('.', '', 1).isdigit(): raise ValueError("Цена закупки должна быть числом")
            if not sell_str.replace('.', '', 1).isdigit(): raise ValueError("Цена продажи должна быть числом")
            if not qty_str.isdigit(): raise ValueError("Количество должно быть числом")

            buy_price = float(buy_str)
            sell_price = float(sell_str)
            qty = int(qty_str)

            if buy_price < 0 or sell_price < 0: raise ValueError("Цены не могут быть отрицательными")

            products.append(Product(name, buy_price, sell_price, qty))
            print("Товар добавлен.")
        except ValueError as e: print("Ошибка: " + str(e))

    elif sub == "2":
        for p in products:
            print(f"ID: {p.get_id()} | {p.get_name()} | Закупка: {p.get_purchase_price()} | Продажа: {p.get_selling_price()} | Всего: {p.get_quantity()}")

def manage_warehouses(warehouses, products):
    print("\n--- Склады ---")
    print("1. Создать | 2. Добавить ячейку | 3. Отчет | 4. Положить товар | 5. Списать | 6. Переместить")
    sub = input("Выбор: ").strip()

    if sub == "1":
        name = input("Название склада: ").strip()
        addr = input("Адрес: ").strip()
        warehouses.append(Warehouse(name, addr))

    elif sub == "2":
        try:
            wid = int(input("ID склада: "))
            wh = next((w for w in warehouses if w.get_id() == wid), None)
            if wh:
                num = input("Номер ячейки: ").strip()
                wh.add_cell(num)
                print("Ячейка добавлена.")
        except ValueError: print("Ошибка: ID должен быть числом.")

    elif sub == "3":
        for w in warehouses:
            print(w.get_info())
            print(WarehouseService.get_full_stock_report(w))

    elif sub == "4":
        try:
            wid = int(input("ID склада: "))
            wh = next((w for w in warehouses if w.get_id() == wid), None)
            if not wh: print("Склад не найден"); return

            cid = int(input("ID ячейки: "))
            pid = int(input("ID товара: "))
            qty = int(input("Количество: "))

            WarehouseService.add_stock(wh, cid, pid, qty, products)
            print("Товар добавлен в ячейку.")
        except ValueError as e: print("Ошибка: " + str(e))

    elif sub == "5":
        try:
            wid = int(input("ID склада: "))
            wh = next((w for w in warehouses if w.get_id() == wid), None)
            if not wh: print("Склад не найден"); return

            cid = int(input("ID ячейки: "))
            pid = int(input("ID товара: "))
            qty = int(input("Количество: "))

            WarehouseService.remove_stock(wh, cid, pid, qty, products)
            print("Товар списан.")
        except ValueError as e: print("Ошибка: " + str(e))

    elif sub == "6":
        try:
            wid = int(input("ID склада: "))
            wh = next((w for w in warehouses if w.get_id() == wid), None)
            if not wh: print("Склад не найден"); return

            pid = int(input("ID товара: "))
            qty = int(input("Количество: "))
            f_cid = int(input("Из ячейки ID: "))
            t_cid = int(input("В ячейку ID: "))

            WarehouseService.move_product(wh, pid, qty, f_cid, t_cid)
            print("Товар перемещен.")
        except ValueError as e: print("Ошибка: " + str(e))


def manage_sales_points(sales_points, employees):
    print("\n--- Пункты продаж ---")
    print("1. Создать | 2. Открыть/Закрыть | 3. Список | 4. Назначить ответственного")
    sub = input("Выбор: ").strip()

    if sub == "1":
        name = input("Название ПП: ").strip()
        if not name:
            print("Ошибка: Название не может быть пустым")
            return

        addr = input("Адрес ПП: ").strip()
        if not addr:
            print("Ошибка: Адрес не может быть пустым")
            return

        sp = SalesPoint(name, addr)
        sales_points.append(sp)
        print(f"ТТ создана с ID: {sp.get_id()}")

    elif sub == "2":
        try:
            spid = int(input("ID торговой точки: "))
            sp = next((s for s in sales_points if s.get_id() == spid), None)
            if not sp:
                print("Точка не найдена")
                return

            print(f"Текущий статус: {'Открыт' if sp.get_is_active() else 'Закрыт'}")
            act = input("1 - Открыть, 0 - Закрыть: ").strip()

            if act == "1":
                sp.open()
                print("Точка открыта")
            elif act == "0":
                sp.close()
                print("Точка закрыта")
            else:
                print("Ошибка: Неверный выбор")
        except ValueError:
            print("Ошибка: ID должен быть числом")

    elif sub == "3":
        if not sales_points:
            print("Список пуст")
        else:
            print("\n=== Список торговых точек ===")
            for sp in sales_points:
                print(sp.get_info())
                print(f"  Остатки товаров: {sp.get_products()}")
            print("==========================")

    elif sub == "4":
        try:
            spid = int(input("ID торговой точки: "))
            sp = next((s for s in sales_points if s.get_id() == spid), None)
            if not sp:
                print("Точка не найдена")
                return

            eid = int(input("ID сотрудника: "))
            emp = next((e for e in employees if e.get_id() == eid), None)
            if not emp:
                print("Сотрудник не найден")
                return

            if not emp.get_is_active():
                print("Ошибка: Сотрудник уволен")
                return

            sp.change_responsible(emp.get_id())
            print("Ответственный назначен")
        except ValueError:
            print("Ошибка: ID должен быть числом")


def manage_sales(sales_points, customers, orders, products):
    print("\n--- Операции с товарами ---")
    print("1. Продажа клиенту")
    print("2. Закупка товара на торговую точку (Поставка)")
    print("3. Возврат товара от клиента")
    sub = input("Выбор: ").strip()

    def find_point():
        try:
            spid = int(input("ID торговой точки: "))
            sp = next((s for s in sales_points if s.get_id() == spid), None)
            if not sp:
                print("Точка не найдена.")
            return sp
        except ValueError:
            print("Ошибка: ID должен быть числом.")
            return None

    def find_customer():
        try:
            cid = int(input("ID клиента: "))
            cust = CustomerService.find_by_id(customers, cid)
            if not cust:
                print("Клиент не найден.")
            return cust
        except ValueError:
            print("Ошибка: ID должен быть числом.")
            return None

    def create_cart():
        cart = []
        print("\n=== Формирование корзины ===")
        print("Вводите товары. Для завершения введите ID товара: 0")

        while True:
            try:
                pid = int(input("\nID товара (0 - завершить): "))
                if pid == 0:
                    if not cart:
                        print("Ошибка: Корзина пуста. Добавьте хотя бы один товар.")
                        continue
                    break

                qty = int(input("Количество: "))
                price = float(input("Цена за шт: "))

                if qty <= 0:
                    print("Ошибка: Количество должно быть больше 0")
                    continue
                if price < 0:
                    print("Ошибка: Цена не может быть отрицательной")
                    continue

                cart.append({"product_id": pid, "quantity": qty, "price": price})
                print(f"✓ Товар {pid} добавлен ({qty} шт. x {price}₽)")

            except ValueError:
                print("Ошибка: Введите корректные числа.")

        print(f"\n✓ Корзина сформирована. Товаров: {len(cart)}")
        return cart

    if sub == "1":
        print("\n--- Продажа ---")
        sp = find_point()
        if not sp:
            return
        cust = find_customer()
        if not cust:
            return

        cart = create_cart()

        try:
            receipt = SalesService.process_sale(sp, cust, cart, orders, products)
            print("\n" + "=" * 40)
            print(SalesService.format_receipt(receipt))
            print("=" * 40)
            print("✓ Продажа успешно оформлена!")
        except ValueError as e:
            print(f"✗ Ошибка: {e}")

    elif sub == "2":
        print("\n--- Закупка товара ---")
        sp = find_point()
        if not sp:
            return

        cart = create_cart()

        try:
            receipt = SalesService.process_purchase(sp, cart, orders, products)
            print("\n" + "=" * 40)
            print(SalesService.format_receipt(receipt))
            print("=" * 40)
            print("✓ Закупка успешно оформлена!")
            print(f"✓ Текущие остатки точки: {sp.get_products()}")
        except ValueError as e:
            print(f"✗ Ошибка: {e}")

    elif sub == "3":
        print("\n--- Возврат товара ---")
        sp = find_point()
        if not sp:
            return
        cust = find_customer()
        if not cust:
            return

        cart = create_cart()

        try:
            receipt = SalesService.process_return(sp, cust, cart, orders, products)
            print("\n" + "=" * 40)
            print(SalesService.format_receipt(receipt))
            print("=" * 40)
            print("✓ Возврат успешно оформлен!")
        except ValueError as e:
            print(f"✗ Ошибка: {e}")
    else:
        print("Неверный выбор операции.")

if __name__ == "__main__":
    main()