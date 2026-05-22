from abc import ABC, abstractmethod
import json
import os
from models.employee import Employee
from models.customer import Customer
from models.product import Product
from models.warehouse import Warehouse
from models.warehouse_cell import WarehouseCell
from models.sales_point import SalesPoint
from models.order import Order
from models.person import Person

class BaseSerializer(ABC):
    @abstractmethod
    def serialize_object(self, items: list):
        pass

class BaseDeserializer(ABC):
    @abstractmethod
    def deserialize_object(self):
        pass

class FileInfo:
    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__format_of_file = None

    def set_filename(self, file_name: str):
        self.__file_name = file_name

    def get_filename(self):
        return self.__file_name

    def set_format_of_file(self, fmt: str):
        self.__format_of_file = fmt

    def get_format_of_file(self):
        return self.__format_of_file

    def get_full_file_name(self) -> str:
        base = os.path.join("storage", "data", self.__file_name)
        return f"{base}.{self.__format_of_file}" if self.__format_of_file else base

class BaseJSONParser(FileInfo, BaseSerializer, BaseDeserializer):
    def __init__(self, file_name: str):
        super().__init__(file_name)
        self.set_format_of_file('json')

    def serialize_object(self, items: list):
        path = self.get_full_file_name()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            data = [self.to_dict(item) for item in items]
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Сохранено {len(items)} записей: {path}")
        except Exception as e:
            print(f"Ошибка сохранения {path}: {e}")

    def deserialize_object(self):
        path = self.get_full_file_name()
        if not os.path.exists(path):
            return []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw = json.load(f)
            print(f"Загружено {len(raw)} записей из {path}")
            return [self.from_dict(item) for item in raw]
        except Exception as e:
            print(f"Ошибка загрузки {path}: {e}")
            return []

    @abstractmethod
    def to_dict(self, item):
        pass

    @abstractmethod
    def from_dict(self, data):
        pass

class EmployeeParser(BaseJSONParser):
    def __init__(self):
        super().__init__("employees")

    def to_dict(self, e):
        return {"_id": e.get_id(), "_full_name": e.get_full_name(), "_phone": e.get_phone(),
                "_passport_data": e.get_passport_data(), "_date_of_birth": e.get_date_of_birth(),
                "_position": e.get_position(), "_salary": e.get_salary(), "_is_active": e.get_is_active()}

    def from_dict(self, d):
        obj = Employee(d["_full_name"], d["_phone"], d["_passport_data"], d["_date_of_birth"], d["_position"], d["_salary"])
        obj._id = d.get("_id", 0)
        obj._is_active = d.get("_is_active", True)
        Person._id_counter = max(Person._id_counter, d.get("_id", 0) + 1)
        return obj

class CustomerParser(BaseJSONParser):
    def __init__(self):
        super().__init__("customers")

    def to_dict(self, c):
        return {"_id": c.get_id(), "_full_name": c.get_full_name(), "_phone": c.get_phone(),
                "_passport_data": c.get_passport_data(), "_date_of_birth": c.get_date_of_birth(),
                "_sales_point_address": c.get_sales_point_address()}

    def from_dict(self, d):
        obj = Customer(d["_full_name"], d["_phone"], d["_passport_data"], d["_date_of_birth"], d.get("_sales_point_address", ""))
        obj._id = d.get("_id", 0)
        Person._id_counter = max(Person._id_counter, d.get("_id", 0) + 1)
        return obj

class ProductParser(BaseJSONParser):
    def __init__(self):
        super().__init__("products")

    def to_dict(self, p):
        return {"_id": p.get_id(), "_name": p.get_name(), "_purchase_price": p.get_purchase_price(),
                "_selling_price": p.get_selling_price(), "_quantity": p.get_quantity()}

    def from_dict(self, d):
        obj = Product(d["_name"], d["_purchase_price"], d["_selling_price"], d["_quantity"])
        obj._id = d.get("_id", 0)
        Product._id_counter = max(Product._id_counter, d.get("_id", 0) + 1)
        return obj

class WarehouseParser(BaseJSONParser):
    def __init__(self):
        super().__init__("warehouses")

    def to_dict(self, w):
        return {"_id": w.get_id(), "_name": w.get_name(), "_address": w.get_address(),
                "_responsible_person_id": w.get_responsible_person_id(),
                "_cells": [c.__dict__ for c in w.get_cells()], "_is_active": w.get_is_active()}

    def from_dict(self, d):
        obj = Warehouse(d["_name"], d["_address"])
        obj._id = d.get("_id", 0)
        obj._is_active = d.get("_is_active", True)
        if "_responsible_person_id" in d:
            obj._responsible_person_id = d["_responsible_person_id"]
        for cd in d.get("_cells", []):
            cell = WarehouseCell(cd["_warehouse_id"], cd["_cell_number"])
            cell._id = cd.get("_id", 0)
            cell._products = cd.get("_products", {})
            obj._cells.append(cell)
        Warehouse._id_counter = max(Warehouse._id_counter, d.get("_id", 0) + 1)
        return obj

class SalesPointParser(BaseJSONParser):
    def __init__(self):
        super().__init__("sales_points")

    def to_dict(self, sp):
        return {"_id": sp.get_id(), "_name": sp.get_name(), "_address": sp.get_address(),
                "_responsible_person_id": sp.get_responsible_person_id(), "_products": sp.get_products(),
                "_is_active": sp.get_is_active(), "_revenue": sp.get_revenue()}

    def from_dict(self, d):
        obj = SalesPoint(d["_name"], d["_address"])
        obj._id = d.get("_id", 0)
        obj._is_active = d.get("_is_active", True)
        obj._revenue = d.get("_revenue", 0.0)
        if "_responsible_person_id" in d:
            obj._responsible_person_id = d["_responsible_person_id"]
        obj._products = d.get("_products", {})
        SalesPoint._id_counter = max(SalesPoint._id_counter, d.get("_id", 0) + 1)
        return obj


class OrderParser(BaseJSONParser):
    def __init__(self):
        super().__init__("orders")

    def to_dict(self, o):
        return {"_id": o.get_id(), "_customer_id": o.get_customer_id(), "_sales_point_id": o.get_sales_point_id(),
                "_products": o.get_products(), "_date": o.get_date(), "_order_type": o.get_order_type()}

    def from_dict(self, d):
        obj = Order(d["_customer_id"], d["_sales_point_id"], d.get("_order_type", "sale"))
        obj._id = d.get("_id", 0)
        obj._date = d.get("_date", "")

        for p in d.get("_products", []):
            p_price = p.get("purchase_price", 0.0)
            obj.add_product(p["product_id"], p["quantity"], p["price"], p_price)

        Order._id_counter = max(Order._id_counter, d.get("_id", 0) + 1)
        return obj

class FileHandler:
    def __init__(self):
        self._parsers = {
            "employees": EmployeeParser(),
            "customers": CustomerParser(),
            "products": ProductParser(),
            "warehouses": WarehouseParser(),
            "sales_points": SalesPointParser(),
            "orders": OrderParser()
        }

    def save_all(self, employees, customers, products, warehouses, sales_points, orders):
        print("Сохранение данных")
        self._parsers["employees"].serialize_object(employees)
        self._parsers["customers"].serialize_object(customers)
        self._parsers["products"].serialize_object(products)
        self._parsers["warehouses"].serialize_object(warehouses)
        self._parsers["sales_points"].serialize_object(sales_points)
        self._parsers["orders"].serialize_object(orders)
        print("Сохранение завершено.")

    def load_all(self):
        print("Загрузка данных")
        employees = self._parsers["employees"].deserialize_object()
        customers = self._parsers["customers"].deserialize_object()
        products = self._parsers["products"].deserialize_object()
        warehouses = self._parsers["warehouses"].deserialize_object()
        sales_points = self._parsers["sales_points"].deserialize_object()
        orders = self._parsers["orders"].deserialize_object()
        print("Загрузка завершена.")
        return employees, customers, products, warehouses, sales_points, orders