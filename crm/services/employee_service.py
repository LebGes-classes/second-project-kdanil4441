from models.employee import Employee

class EmployeeService:

    @staticmethod
    def hire(employees_list, full_name, phone, passport_data, date_of_birth, position, salary):
        new_employee = Employee(full_name, phone, passport_data, date_of_birth, position, salary)
        employees_list.append(new_employee)
        return new_employee

    @staticmethod
    def fire(employee):
        if not employee.get_is_active():
            raise ValueError("Сотрудник уже уволен.")
        employee.fire()

    @staticmethod
    def set_warehouse_responsible(warehouse, employee):
        if not employee.get_is_active():
            raise ValueError("Нельзя назначить уволенного сотрудника ответственным за склад.")
        warehouse.change_responsible(employee.get_id())

    @staticmethod
    def set_sales_point_responsible(sales_point, employee):
        if not employee.get_is_active():
            raise ValueError("Нельзя назначить уволенного сотрудника ответственным за пункт продаж.")
        sales_point.change_responsible(employee.get_id())

    @staticmethod
    def clear_warehouse_responsible(warehouse):
        warehouse.change_responsible(None)

    @staticmethod
    def clear_sales_point_responsible(sales_point):
        sales_point.change_responsible(None)