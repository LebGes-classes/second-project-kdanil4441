from models.customer import Customer

class CustomerService:

    @staticmethod
    def add_customer(customers_list, full_name, phone, passport_data, date_of_birth, sales_point_address):
        new_customer = Customer(full_name, phone, passport_data, date_of_birth, sales_point_address)
        customers_list.append(new_customer)
        return new_customer

    @staticmethod
    def find_by_id(customers_list, customer_id):
        for customer in customers_list:
            if customer.get_id() == customer_id:
                return customer
        return None

    @staticmethod
    def update_address(customer, new_address):
        if not new_address or not new_address.strip():
            raise ValueError("Адрес не может быть пустым")
        customer.set_sales_point_address(new_address)

    @staticmethod
    def get_purchase_history(customer_id, orders_list):
        return [order for order in orders_list if order.get_customer_id() == customer_id and order.get_order_type() == "sale"]