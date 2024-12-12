from OrdersAdapter import OrdersAdapter

file_for_valid_orders = "order_country.txt"
file_for_non_valid_orders = "non_valid_orders.txt"
file_for_reading_orders = "orders.txt"

order_adapter = OrdersAdapter(file_for_valid_orders=file_for_valid_orders,
                              file_for_non_valid_orders=file_for_non_valid_orders,
                              file_for_reading_orders=file_for_reading_orders)

order_adapter.control_orders()