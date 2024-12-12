import typing as tp
import re
from collections import Counter
import codecs


class Order:
    def __init__(self, order_data: tp.List[str]):
        self.order_id = order_data[0]
        self.goods_list = order_data[1]
        self.customer_name = order_data[2]
        self.order_address = order_data[3]
        self.phone_number = order_data[4]
        self.order_priority = order_data[5]


    def is_valid_phone_number(self):
        number_pattern = r'^\+\d-\d{3}-\d{3}-\d{2}-\d{2}$'
        return re.match(number_pattern, self.phone_number) is not None


    def is_valid_order_address(self):
        try:
            split_address = self.order_address.split(". ")
            return len(split_address) == 4
        except:
            return False


    def collect_multi_goods(self, good_str):
        goods_arr = good_str.split(", ")
        counted_goods = Counter(goods_arr)
        new_str_goods = ", ".join(f"{item} x{cnt}" if cnt > 1 else item for item, cnt in counted_goods.items())
        return new_str_goods


    def collect_order_in_str(self):
        return ";".join((self.order_id, self.goods_list, self.customer_name,
                         self.order_address, self.phone_number, self.order_priority))



class OrdersAdapter:
    def __init__(self, orders_data: tp.List[Order] = None, file_for_reading_orders = None,
                 file_for_non_valid_orders = None, file_for_valid_orders = None):

        self.orders_data = []
        self.file_for_non_valid_orders = file_for_non_valid_orders
        self.file_for_valid_orders = file_for_valid_orders

        self.valid_orders = []
        self.non_valid_orders = []

        if orders_data:
            self.orders_data = orders_data
        elif file_for_reading_orders:
            self.orders_data = self.read_orders_from_file(file_for_reading_orders)


    def read_orders_from_file(self, file):
        temp_orders_data = []
        with codecs.open(file, encoding="utf_8_sig") as f:
            for line in f:
                temp_orders_data.append(Order(line.strip().split(";")))
        return temp_orders_data


    def __key_for_sort(self, order):
        dict_key = {"MAX": 0, "MIDDLE": 1, "LOW": 2}

        country_order_name = order.order_address.split(". ")[0]
        country_priority = 0 if country_order_name == "Россия" else 1
        return country_priority, country_order_name, dict_key[order.order_priority]


    def sort_valid_orders_by_country_priority(self, orders):
         return sorted(orders, key=self.__key_for_sort)


    def sort_orders_by_validity(self):
        for order in self.orders_data:
            if order.is_valid_order_address() and order.is_valid_phone_number():
                self.valid_orders.append(order)
            else:
                self.non_valid_orders.append(order)


    def write_valid_order(self):
        sorted_valid_orders = self.sort_valid_orders_by_country_priority(self.valid_orders)
        with codecs.open(self.file_for_valid_orders, mode='w', encoding="utf_8_sig") as f:
            for order in sorted_valid_orders:
                order.goods_list = order.collect_multi_goods(order.goods_list)
                order.order_address = ". ".join(order.order_address.split(". ")[1:])
                print(order.collect_order_in_str(), file=f)


    def write_non_valid_order(self):
        with codecs.open(self.file_for_non_valid_orders, mode='w', encoding="utf_8_sig") as f:
            for order in self.non_valid_orders:
                if not order.is_valid_order_address():
                    error_data = order.order_address if order.order_address else "no data"
                    print(f"{order.order_id};1;{error_data}", file=f)
                if not order.is_valid_phone_number():
                    error_data = order.phone_number if order.phone_number else "no data"
                    print(f"{order.order_id};2;{error_data}", file=f)


    def control_orders(self):
        self.sort_orders_by_validity()
        self.write_valid_order()
        self.write_non_valid_order()





























