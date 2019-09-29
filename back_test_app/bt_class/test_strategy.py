
from .indicators_obj import *

import random

class Signal():
    def __init__(self, bt_data):
        self.signal_list = list()

    def reset(self):
        self.signal_list = []

    def sell(self):
        date = random.randint(20180703092000, 20190703092000)
        price = random.randint(500, 2000)

        self.signal_list.append({'date':date, 'price':price, 'action':'sell'})

    def buy(self):
        date = random.randint(20180703092000, 20190703092000)
        price = random.randint(500, 2000)
        self.signal_list.append({'date': date, 'price': price, 'action': 'buy'})

    def hold(self):
        date = random.randint(20180703092000, 20190703092000)
        price = random.randint(500, 2000)
        self.signal_list.append({'date': date, 'price': price, 'action': 'hold'})

    def get_signal(self, sort_type='asc'):

        return self.signal_list


class BackTest_Data():
    def __init__(self):
        self.__origin_candle_count = 10
        self.base_index = 1

    def set_base_index(self, base_index):
        self.base_index = base_index

    def get_origin_candle_count(self):
        return self.__origin_candle_count


class TestStrategy:
    def __init__(self):
        self.bt_data = BackTest_Data()
        self.run_strategy_error = None
        self.signal = Signal(self.bt_data)

    def run_strategy(self, strategy_variable, strategy_context):
        body_1 = '''

#base_index = self.bt_data.get_base_index()
self.signal.reset()
self.run_strategy_error = None

'''
        body_2 = '''

for i in range(self.bt_data.get_origin_candle_count()):
    self.bt_data.set_base_index(i)

'''
        body_3 = '''

#self.bt_data.set_base_index(base_index)

'''
        nested_str = '    '
        s_v = strategy_variable
        s_c = nested_str + strategy_context.replace('\n', '\n' + nested_str)

        body = body_1 + s_v + body_2 + s_c + body_3
        try:
            exec(body)
        except Exception as e:
            self.run_strategy_error = str(e.args)

        return self.run_strategy_error
