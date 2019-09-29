
from .constant import constant
import random

over_coeff = 10

class Data():
    def __init__(self, bt_data):
        self.bt_data = bt_data

    def get_data(self, candle_index, candle_count=1, data_type=None, get_error=False):

        res = list()
        for i in range(candle_count):
            res.append(random.randint(500, 2000))


        if data_type == constant.ts_data_type_all:
            for i in range(candle_count):
                res.append([random.randint(500, 2000), random.randint(500, 2000), random.randint(500, 2000), random.randint(500, 2000),
                            random.randint(500, 2000), random.randint(500, 2000), random.randint(500, 2000), random.randint(500, 2000)])

        else:
            for i in range(candle_count):
                res.append(random.randint(500, 2000))


        if get_error is True:
            return res, None
        else:
            return res


class SMA():
    def __init__(self, period, bt_data):
        self.obj_error = None
        self.period = period
        #self.bt_data:BackTest_Data = bt_data
        self.bt_data = bt_data

    def d(self, candle_index, data_type=None, get_error=False):

        res = random.randint(500, 2000)
        # ----------------------------
        if get_error is True:
            return res, None
        else:
            return res


class SMA_list():
    def __init__(self, period, bt_data):
        self.obj_error = None
        self.period = period
        self.bt_data = bt_data

    def d(self, candle_index, list_count, data_type=None, get_error=False):
        res = list()
        for i in range(list_count):
            res.append(random.randint(500, 2000))
        # ----------------------------
        if get_error is True:
            return res, None
        else:
            return res


class EMA():
    def __init__(self, period, bt_data):
        self.obj_error = None
        self.period = period
        self.bt_data = bt_data

    def d(self, candle_index, data_type=None, get_error=False):
        res = random.randint(500, 2000)
        # ----------------------------
        if get_error is True:
            return res, None
        else:
            return res


class EMA_list():
    def __init__(self, period, bt_data):
        self.obj_error = None
        self.period = period
        self.bt_data = bt_data

    def d(self, candle_index, list_count, data_type=None, get_error=False):
        res = list()
        for i in range(list_count):
            res.append(random.randint(500, 2000))
        # ----------------------------
        if get_error is True:
            return res, None
        else:
            return res


class SMMA():
    def __init__(self, period, bt_data):
        self.obj_error = None
        self.period = period
        self.bt_data = bt_data

    def d(self, candle_index, data_type=None, get_error=False):
        res = random.randint(500, 2000)
        # ----------------------------
        if get_error is True:
            return res, None
        else:
            return res


class SMMA_list():
    def __init__(self, period, bt_data):
        self.obj_error = None
        self.period = period
        self.bt_data = bt_data

    def d(self, candle_index, list_count, data_type=None, get_error=False):
        res = list()
        for i in range(list_count):
            res.append(random.randint(500, 2000))
        # ----------------------------
        if get_error is True:
            return res, None
        else:
            return res


class LWMA():
    def __init__(self, period, bt_data):
        self.obj_error = None
        self.period = period
        self.bt_data = bt_data

    def d(self, candle_index, data_type=None, get_error=False):
        res = random.randint(500, 2000)
        # ----------------------------
        if get_error is True:
            return res, None
        else:
            return res


class LWMA_list():
    def __init__(self, period, bt_data):
        self.obj_error = None
        self.period = period
        self.bt_data = bt_data

    def d(self, candle_index, list_count, data_type=None, get_error=False):
        res = list()
        for i in range(list_count):
            res.append(random.randint(500, 2000))
        # ----------------------------
        if get_error is True:
            return res, None
        else:
            return res


class MACD():
    def __init__(self, slow_period, fast_period, macd_period, bt_data):
        self.last_data = None

    def d(self, candle_index, data_type=None, get_error=False):
        fast_point = random.randint(500, 2000)
        slow_point = random.randint(500, 2000)
        macd_line = random.randint(500, 2000)
        signal_line = random.randint(500, 2000)
        macd_histogram = macd_line - signal_line

        res = {'slow': slow_point, 'fast': fast_point, 'signal_line': signal_line,
               'macd_line': macd_line, 'macd_histogram': macd_histogram}

        self.last_data = res

        if get_error is True:
            return res, None
        else:
            return res

    def slow(self, candle_index, data_type=None, get_error=False):
        error = None
        if get_error is True:
            d_res, error = self.d(candle_index, data_type, get_error)
        else:
            d_res = self.d(candle_index, data_type, get_error)

        try:
            res = d_res['slow']
        except:
            res = None

        if get_error is True:
            return res, error
        else:
            return res

    def fast(self, candle_index, data_type=None, get_error=False):
        error = None
        if get_error is True:
            d_res, error = self.d(candle_index, data_type, get_error)
        else:
            d_res = self.d(candle_index, data_type, get_error)

        try:
            res = d_res['fast']
        except:
            res = None

        if get_error is True:
            return res, error
        else:
            return res

    def signal_line(self, candle_index, data_type=None, get_error=False):
        error = None
        if get_error is True:
            d_res, error = self.d(candle_index, data_type, get_error)
        else:
            d_res = self.d(candle_index, data_type, get_error)

        try:
            res = d_res['signal_line']
        except:
            res = None

        if get_error is True:
            return res, error
        else:
            return res

    def macd_line(self, candle_index, data_type=None, get_error=False):
        error = None
        if get_error is True:
            d_res, error = self.d(candle_index, data_type, get_error)
        else:
            d_res = self.d(candle_index, data_type, get_error)

        try:
            res = d_res['macd_line']
        except:
            res = None

        if get_error is True:
            return res, error
        else:
            return res

    def macd_histogram(self, candle_index, data_type=None, get_error=False):
        error = None
        if get_error is True:
            d_res, error = self.d(candle_index, data_type, get_error)
        else:
            d_res = self.d(candle_index, data_type, get_error)

        try:
            res = d_res['macd_histogram']
        except:
            res = None

        if get_error is True:
            return res, error
        else:
            return res


class MACD_list():
    def __init__(self, slow_period, fast_period, macd_period, bt_data):
        self.obj_error = None
        self.slow_period = slow_period
        self.fast_period = fast_period
        self.macd_period = macd_period
        self.bt_data = bt_data

        self.last_data = None
        self.last_error = None

    def d(self, candle_index, list_count, data_type=None, get_error=False):
        if self.last_data is not None:
            if list_count <= len(self.last_data):
                if get_error is True:
                    return self.last_data[:list_count], self.last_error
                else:
                    return self.last_data[:list_count]

        res_list = list()
        for i in range(list_count):
            fast_point = random.randint(500, 2000)
            slow_point = random.randint(500, 2000)
            macd_line = random.randint(500, 2000)
            signal_line = random.randint(500, 2000)
            macd_histogram = macd_line - signal_line

            res = {'slow': slow_point, 'fast': fast_point, 'signal_line': signal_line,
                   'macd_line': macd_line, 'macd_histogram': macd_histogram}

            res_list.append(res)

        # ----------------------------------------
        self.last_data = res_list

        if get_error is True:
            return res_list, None
        else:
            return res_list

    def slow(self, candle_index, list_count, data_type=None, get_error=False):
        res, error = self.d(candle_index, list_count + 1, data_type, True)
        res = res[:-1]

        res_list = list()
        for i in range(len(res)):
            if get_error is True:
                try:
                    res_list.append([res[i][0]['slow'], res[i][1]])
                except Exception as e:
                    res_list.append([None, str(res[i][1]) + ' : ' + str(e)])
            else:
                try:
                    res_list.append(res[i][0]['slow'])
                except:
                    res_list.append(None)

        if get_error is True:
            return res_list, error
        else:
            return res_list

    def fast(self, candle_index, list_count, data_type=None, get_error=False):
        res, error = self.d(candle_index, list_count + 1, data_type, True)
        res = res[:-1]

        res_list = list()
        for i in range(len(res)):
            if get_error is True:
                try:
                    res_list.append([res[i][0]['fast'], res[i][1]])
                except Exception as e:
                    res_list.append([None, str(res[i][1]) + ' : ' + str(e)])
            else:
                try:
                    res_list.append(res[i][0]['fast'])
                except:
                    res_list.append(None)

        if get_error is True:
            return res_list, error
        else:
            return res_list

    def signal_line(self, candle_index, list_count, data_type=None, get_error=False):
        res, error = self.d(candle_index, list_count + 1, data_type, True)
        res = res[:-1]

        res_list = list()
        for i in range(len(res)):
            if get_error is True:
                try:
                    res_list.append([res[i][0]['signal_line'], res[i][1]])
                except Exception as e:
                    res_list.append([None, str(res[i][1]) + ' : ' + str(e)])
            else:
                try:
                    res_list.append(res[i][0]['signal_line'])
                except:
                    res_list.append(None)

        if get_error is True:
            return res_list, error
        else:
            return res_list

    def macd_line(self, candle_index, list_count, data_type=None, get_error=False):
        res, error = self.d(candle_index, list_count + 1, data_type, True)
        res = res[:-1]

        res_list = list()
        for i in range(len(res)):
            if get_error is True:
                try:
                    res_list.append([res[i][0]['macd_line'], res[i][1]])
                except Exception as e:
                    res_list.append([None, str(res[i][1]) + ' : ' + str(e)])
            else:
                try:
                    res_list.append(res[i][0]['macd_line'])
                except:
                    res_list.append(None)

        if get_error is True:
            return res_list, error
        else:
            return res_list

    def macd_histogram(self, candle_index, list_count, data_type=None, get_error=False):
        res, error = self.d(candle_index, list_count + 1, data_type, True)
        res = res[:-1]

        res_list = list()
        for i in range(len(res)):
            if get_error is True:
                try:
                    res_list.append([res[i][0]['macd_histogram'], res[i][1]])
                except Exception as e:
                    res_list.append([None, str(res[i][1]) + ' : ' + str(e)])
            else:
                try:
                    res_list.append(res[i][0]['macd_histogram'])
                except:
                    res_list.append(None)

        if get_error is True:
            return res_list, error
        else:
            return res_list


class RSI():
    def __init__(self, period, bt_data):
        self.obj_error = None
        self.period = period
        self.bt_data = bt_data

    def d(self, candle_index, data_type=None, get_error=False):
        res = random.randint(0, 100)
        # ----------------------------
        if get_error is True:
            return res, None
        else:
            return res


class WILLIAMS():
    def __init__(self, period, bt_data):
        self.obj_error = None
        self.period = period
        self.bt_data = bt_data

    def d(self, candle_index, data_type=None, get_error=False):
        res = random.randint(100, 1000)
        # ----------------------------
        if get_error is True:
            return res, None
        else:
            return res
