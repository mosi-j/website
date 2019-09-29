import pymysql
from .Log import *
#import constant
from .constant import constant
from .my_time import get_now_time_second



class Database:

    def __init__(self, db_info, log_obj=None):
        try:
            if log_obj is None:
                self.log = Logging()
                self.log.logConfig(account_id=db_info['db_username'])
            else:
                self.log = log_obj

            self.log.trace()
            self.db_host_name = db_info['db_host_name']
            self.db_username = db_info['db_username']
            self.db_user_password = db_info['db_user_password']
            self.db_name = db_info['db_name']
            self.db_port = db_info['db_port']

        except Exception as e:
            self.log.error('cant create database object: ', str(e))
            return

    def get_connection(self, ):
        try:
            if self.db_port is None:
                con = pymysql.connect(host=self.db_host_name, user=self.db_username,
                                      password=self.db_user_password, db=self.db_name)
            else:
                con = pymysql.connect(host=self.db_host_name, user=self.db_username, password=self.db_user_password,
                                      db=self.db_name, port=self.db_port)
            return con, None
        except Exception as e:
            self.log.error('cant create connection: ', str(e))
            return False, str(e)

    def select_query(self, query, args, mod=0):
        # mod=0 => return cursor
        # mod=1 => retyrn cursor.fetchall()
        error = None
        self.log.trace()
        if query == '':
            self.log.error('query in empty')
            error = 'SQL ERROR: query in empty'
            return False, error

        con = None
        try:
            con, err = self.get_connection()
            if err is not None:
                raise Exception(err)
            db = con.cursor()
            db.execute(query, args)
            con.close()
        except Exception as e:
            self.log.error('except select_query', str(e))
            try:
                if con.open is True:
                    con.close()
            finally:
                error = 'SQL ERROR:{0} query:{1} args:{2}'.format(str(e), query, args)
                return False, error

        if mod == 0:
            return db, error
        else:
            return db.fetchall(), error

    def select_query_dictionary(self, query, args, mod=0):
        # mod=0 => return cursor
        # mod=1 => retyrn cursor.fetchall()
        error = None
        self.log.trace()
        if query == '':
            self.log.error('query in empty')
            error = 'SQL ERROR: query in empty'
            return False, error
        con = None
        try:
            con, err = self.get_connection()
            if err is not None:
                raise Exception(err)
            db = con.cursor(pymysql.cursors.DictCursor)
            db.execute(query, args)
            con.close()
        except Exception as e:
            self.log.error('except select_query_dictionary', str(e))
            try:
                if con.open is True:
                    con.close()
            finally:
                error = 'SQL ERROR:{0} query:{1} args:{2}'.format(str(e), query, args)
                return False, error

        if mod == 0:
            return db, error
        else:
            return db.fetchall(), error

    def command_query(self, query, args, write_log=True):
        error = None
        self.log.trace()
        if query == '':
            self.log.error('query in empty')
            error = 'SQL ERROR: query in empty'
            return False, error
        con = None
        try:
            con, err = self.get_connection()
            if err is not None:
                raise Exception(err)

            db = con.cursor()
            db._defer_warnings = True
            db.autocommit = False
            db.execute(query, args)
            # db.executemany(query, args)
            con.commit()
            con.close()
            return True, None
        except Exception as e:
            if write_log is True:
                self.log.error('command_query. error:{0} query:{1}, args:{2}'.format(e, query, args))
            try:
                if con.open is True:
                    con.rollback()
                    con.close()
            finally:
                error = 'SQL ERROR:{0} query:{1} args:{2}'.format(str(e), query, args)
                return False, error

    def command_query_many(self, query, args, write_log=True):
        error = None
        self.log.trace()
        if query == '':
            self.log.error('query in empty')
            error = 'SQL ERROR: query in empty'
            return False, error
        con = None
        try:
            con, err = self.get_connection()
            if err is not None:
                raise Exception(err)

            db = con.cursor()
            db._defer_warnings = True
            db.autocommit = False
            # db.execute(query, args)
            db.executemany(query, args)
            con.commit()
            con.close()
            return True, error
        except Exception as e:
            if write_log is True:
                self.log.error('command_query_many. error:{0} query:{1}, args:{2}'.format(e, query, args))
            try:
                if con.open is True:
                    con.rollback()
                    con.close()
            finally:
                error = 'SQL ERROR:{0} query:{1} args:{2}'.format(str(e), query, args)
                return False, error

    # --------------------------------------------------------------
    def get_share_second_data(self, en_symbol_12_digit_code, start_date_time, end_date_time):
        query = 'select date_time, open_price, close_price, high_price, low_price,' \
                ' trade_count, trade_volume, trade_value from share_second_data ' \
                'where en_symbol_12_digit_code = %s and date_time >= %s and  date_time < %s ' \
                'order by date_time desc'

        args = (en_symbol_12_digit_code, start_date_time, end_date_time)

        return self.select_query(query, args, 1)

    def get_adjusted_data(self, en_symbol_12_digit_code, adjust_type):
        if adjust_type == constant.adjusted_type_none:
            res = list()
            return res, None

        elif adjust_type == constant.adjusted_type_capital_increase:
            query = 'select do_data, coefficient from  share_adjusted_data ' \
                    'where en_symbol_12_digit_code = %s and adjusted_type = %s order by do_data desc'
            args = (en_symbol_12_digit_code, constant.adjusted_type_capital_increase)

        elif adjust_type == constant.adjusted_type_take_profit:
            query = 'select do_data, coefficient from  share_adjusted_data ' \
                    'where en_symbol_12_digit_code = %s and adjusted_type = %s order by do_data desc'
            args = (en_symbol_12_digit_code, constant.adjusted_type_take_profit)

        elif adjust_type == constant.adjusted_type_all:
            query = 'select do_data, coefficient from  share_adjusted_data ' \
                    'where en_symbol_12_digit_code = %s order by do_data desc'
            args = en_symbol_12_digit_code

        else:
            return False, 'invalid adjusted type'

        return self.select_query(query, args, 1)

    def get_benefit_adjusted_data(self, en_symbol_12_digit_code):
        query = 'select do_data, coefficient, adjusted_type, old_data, new_data from  share_adjusted_data ' \
                'where en_symbol_12_digit_code = %s order by do_data desc'

        args = en_symbol_12_digit_code

        return self.select_query(query, args, 1)

    def have_any_data(self, en_symbol_12_digit_code, date_time):
        query = 'select count(*) from share_second_data ' \
                'where en_symbol_12_digit_code = %s and date_time < %s'

        args = (en_symbol_12_digit_code, date_time)
        res, error = self.select_query(query, args, 1)
        if error is not None:
            return None, error

        if res[0][0] > 0:
            return True, error
        else:
            return False, error

    def get_valid_date(self):
        query = 'select * from open_days'

        args = ()

        return self.select_query(query, args, 1)

    def get_symbols(self):
        query = 'select en_symbol_12_digit_code, fa_symbol_30_digit_code, fa_symbol_name from share_info ' \
                'where is_active = 1 order by fa_symbol_name'

        args = ()

        return self.select_query(query, args, 1)

    def get_symbols_name(self, en_symbol_12_digit_code):
        query = 'select fa_symbol_name from share_info where en_symbol_12_digit_code = %s'

        args = (en_symbol_12_digit_code)

        return self.select_query(query, args, 1)

    def get_industry(self):
        query = 'select en_index_12_digit_code, industry_code, fa_index_name from index_info order by industry_code'

        args = ()

        return self.select_query(query, args, 1)

    def get_strategy_name_list(self, username):
        query = 'select strategy_name from strategy where user_name=%s order by strategy_name'
        args = (username)

        return self.select_query(query, args, 1)

    def get_strategy_context(self, user_name, strategy_name):
        query = 'select strategy_content, strategy_variable from strategy where user_name = %s and strategy_name = %s'
        args = (user_name, strategy_name)

        return self.select_query(query, args, 1)

    def get_strategy_name(self, user_name, strategy_name):
        query = 'select strategy_name from strategy where user_name = %s and strategy_name = %s'
        args = (user_name, strategy_name)

        return self.select_query(query, args, 1)

    def update_strategy_context(self, user_name, strategy_name, variable, content):
        query = 'update strategy set strategy_variable=%s, strategy_content=%s where user_name = %s and strategy_name = %s'
        args = (variable, content, user_name, strategy_name)

        return self.command_query(query, args, True)

    def insert_strategy(self, user_name, strategy_name, strategy_variable, strategy_content):
        query = 'insert IGNORE  into strategy (user_name, strategy_name, strategy_variable, strategy_content) values (%s, %s, %s, %s)'
        args = (user_name, strategy_name, strategy_variable, strategy_content)

        return self.command_query(query, args, True)

    def exist_strategy_name(self, user_name, strategy_name):
        query = 'select count(*) from strategy where user_name = %s and strategy_name=%s'
        args = (user_name, strategy_name)

        res, err = self.select_query(query, args, 1)
        if err is None:
            if res[0][0] > 0:
                return True
            else:
                return False
        return err

    # -------------------------
    def insert_back_test_result(self, username, start_run_date, run_time, params, outout):
        query = 'insert into back_test_result (username, start_run_date, run_time, params, outout) values (%s, %s, %s, %s, %s)'
        args = (username, start_run_date, run_time, params, outout)

        return self.command_query(query, args, True)

    def get_back_test_result_data(self, username, count):
        query = 'select start_time, order_runtime, input_param, result from back_test_order_result where username = %s ' \
                'order by start_time desc limit %s'
        args = (username, count)

        return self.select_query(query, args, 1)

    def add_order(self, order_id, username, input_param):
        query = 'insert into waiting_order (order_id, username, input_param, add_time, expire_time) values (%s, %s, %s, %s, %s)'
        now_time = get_now_time_second()
        args = (order_id, username, input_param,now_time ,now_time)

        print(now_time)
        print(query)
        print(args)
        return self.command_query(query, args, True)
