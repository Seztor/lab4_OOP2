import unittest
from src.lab4.OrdersAdapter import OrdersAdapter, Order

class OrderTestCase(unittest.TestCase):

    def test_order_is_valid_number_1(self):
        order_data = ("48276;Яблоки, Макароны, Яблоки;Алексеев Алексей Алексеевич;"
                      "Италия. Лацио. Рим. Колизей;+3-061-234-56-78;MAX").split(";")
        order = Order(order_data=order_data)
        self.assertTrue(order.is_valid_phone_number())


    def test_order_is_valid_number_2(self):
        order_data = ("65829;Сок, Вода, Сок, Вода;Белова Екатерина Михайловна;"
                      "Испания. Каталония. Барселона. Рамбла;+34-93-1234-567;LOW").split(";")
        order = Order(order_data=order_data)
        self.assertFalse(order.is_valid_phone_number())


    def test_order_is_valid_address_1(self):
        order_data = ("31987;Сыр, Колбаса, Макароны, Сыр, Колбаса;Петрова Анна Сергеевна;"
                      "Франция. Иль-де-Франс. Париж. Шанз-Элизе;+3-214-020-50-50;MIDDLE").split(";")
        order = Order(order_data=order_data)
        self.assertTrue(order.is_valid_order_address())

    def test_order_is_valid_address_2(self):
        order_data = ("84756;Печенье, Сыр, Печенье, Сыр;Васильева Анна Владимировна;"
                      "Япония. Шибуя. Шибуя-кроссинг;+8-131-234-5678;MAX").split(";")
        order = Order(order_data=order_data)
        self.assertFalse(order.is_valid_order_address())

    def test_order_collect_multi_goods(self):
        order_data = ("87459;Молоко, Яблоки, Хлеб, Яблоки, Молоко;Иванов Иван Иванович;"
                      "Россия. Московская область. Москва. улица Пушкина;+7-912-345-67-89;MAX").split(";")
        order = Order(order_data=order_data)
        check_data = "Молоко x2, Яблоки x2, Хлеб"
        self.assertEqual(order.collect_multi_goods(order.goods_list), check_data)


class OrdersAdapterTestCase(unittest.TestCase):


    def test_check_sorting_by_country_priority(self):
        orders_adapter_1 = OrdersAdapter(file_for_reading_orders="../../src/lab4/orders.txt")
        orders_adapter_1.sort_orders_by_validity()
        orders = orders_adapter_1.valid_orders
        sorted_orders = [order.collect_order_in_str() for order in orders_adapter_1.sort_valid_orders_by_country_priority(orders)]

        list_to_check = ['87459;Молоко, Яблоки, Хлеб, Яблоки, Молоко;Иванов Иван Иванович;Россия. Московская область. Москва. улица Пушкина;+7-912-345-67-89;MAX',
                        '31987;Сыр, Колбаса, Сыр, Макароны, Колбаса;Петрова Анна;Россия. Ленинградская область. Санкт-Петербург. набережная реки Фонтанки;+7-921-456-78-90;MIDDLE',
                        '72901;Чай, Кофе, Чай, Кофе;Михайлов Сергей Петрович;Великобритания. Англия. Лондон. Бейкер-стрит;+4-207-946-09-58;LOW',
                        '48276;Яблоки, Макароны, Яблоки;Алексеев Алексей Алексеевич;Италия. Лацио. Рим. Колизей;+3-061-234-56-78;MAX',
                        '31987;Сыр, Колбаса, Макароны, Сыр, Колбаса;Петрова Анна Сергеевна;Франция. Иль-де-Франс. Париж. Шанз-Элизе;+3-214-020-50-50;MIDDLE']

        self.assertListEqual(sorted_orders, list_to_check)


    def test_check_sorting_by_validity(self):
        orders_adapter_2 = OrdersAdapter(file_for_reading_orders="../../src/lab4/orders.txt")
        orders_adapter_2.sort_orders_by_validity()
        non_valid_orders = [order.collect_order_in_str() for order in orders_adapter_2.non_valid_orders]
        valid_orders = [order.collect_order_in_str() for order in orders_adapter_2.valid_orders]

        list_to_check_non_valid = ['56342;Хлеб, Молоко, Хлеб, Молоко;Смирнова Мария Леонидовна;Германия. Бавария. Мюнхен. Мариенплац;+4-989-234-56;LOW',
                                   '65829;Сок, Вода, Сок, Вода;Белова Екатерина Михайловна;Испания. Каталония. Барселона. Рамбла;+34-93-1234-567;LOW',
                                   '84756;Печенье, Сыр, Печенье, Сыр;Васильева Анна Владимировна;Япония. Шибуя. Шибуя-кроссинг;+8-131-234-5678;MAX',
                                   '90385;Макароны, Сыр, Макароны, Сыр;Николаев Николай;;+1-416-123-45-67;LOW']

        list_to_check_valid = ['31987;Сыр, Колбаса, Сыр, Макароны, Колбаса;Петрова Анна;Россия. Ленинградская область. Санкт-Петербург. набережная реки Фонтанки;+7-921-456-78-90;MIDDLE',
                               '87459;Молоко, Яблоки, Хлеб, Яблоки, Молоко;Иванов Иван Иванович;Россия. Московская область. Москва. улица Пушкина;+7-912-345-67-89;MAX',
                               '31987;Сыр, Колбаса, Макароны, Сыр, Колбаса;Петрова Анна Сергеевна;Франция. Иль-де-Франс. Париж. Шанз-Элизе;+3-214-020-50-50;MIDDLE',
                               '48276;Яблоки, Макароны, Яблоки;Алексеев Алексей Алексеевич;Италия. Лацио. Рим. Колизей;+3-061-234-56-78;MAX',
                               '72901;Чай, Кофе, Чай, Кофе;Михайлов Сергей Петрович;Великобритания. Англия. Лондон. Бейкер-стрит;+4-207-946-09-58;LOW']

        self.assertListEqual(valid_orders, list_to_check_valid)
        self.assertListEqual(non_valid_orders, list_to_check_non_valid)










