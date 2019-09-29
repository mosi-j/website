from django import forms

from .bt_class.constant import *
from .bt_class.new_database import Database
from .bt_class.bt_setting import bt_database_info


class InputParamsForm(forms.Form):
    # def __init__(self, username=None):
    #    super(InputParamsForm, self).__init__()
    #data_count = 0
    time_frame_list = [('S1', 'S1'), ('M1', 'M1'), ('H1', 'H1'), ('D1', 'D1'), ('MN1', 'MN1'), ('Y1', 'Y1')]
    adjusted_mode_list = [(adjusted_mod_now_time, adjusted_mod_now_time)]
    adjusted_type = [(adjusted_type_all, 'سود + افزایش سرمایه'), (adjusted_type_capital_increase, 'افزایش سرمایه'),
                     (adjusted_type_take_profit, 'سود'), (adjusted_type_none, 'تعدیل نشده')]
    data_type_list = [(ts_data_type_open, 'open'), (ts_data_type_close, 'close'),
                      (ts_data_type_high, 'high'), (ts_data_type_low, 'low'),
                      (ts_data_type_weighted, 'weighted'), (ts_data_type_typical, 'typical'),
                      (ts_data_type_median, 'median')]

    db = Database(bt_database_info)

    # get date list -----------------
    valid_date_list = list()
    vdl, err = db.get_valid_date()

    try:
        for item in vdl:
            a = item[0] * 1000000
            s = str(item[1])
            b = s[0:4] + '/' + s[4:6] + '/' + s[6:] + ' : 00:00:00'
            valid_date_list.append((a, b))
    except:
        pass

    # get symbol list -----------------
    invalid_symbol_list = list()
    valid_symbol_list = list()
    symbol_list, err = db.get_symbols()  # en_symbol_12_digit_code, fa_symbol_30_digit_code, fa_symbol_name

    for item in symbol_list:
        if item[0][0:4] == 'IRB6':  # مرابحه
            invalid_symbol_list.append(item[0])
        elif item[0][0:4] == 'IRS5':  # اختیار
            invalid_symbol_list.append(item[0])

    try:
        for item in symbol_list:
            if item[0] in invalid_symbol_list:
                continue

            a = item[0]
            b = str(item[1]) + ' (' + str(item[2]) + ')'
            valid_symbol_list.append((a, b))
    except:
        pass

    # strategy list -----------------
    strategy_list = [('-', 'not choice')]

    output_format_list = [('max_benefit', 'max_benefit'), ('back_test_benefit', 'back_test_benefit'), ('analyze_strategy', 'analyze_strategy')]

    # -------------------
    start_date_time = forms.ChoiceField(label='زمان شروع:', choices=valid_date_list)
    end_date_time = forms.ChoiceField(label='زمان پایان:', choices=valid_date_list)
    time_frame = forms.ChoiceField(label='تایم فریم:', choices=time_frame_list)
    adjusted_type = forms.ChoiceField(label='نوع تعدیل:', choices=adjusted_type)
    max_benefit_up = forms.IntegerField(label='max_benefit_up', min_value=0, initial=1)
    max_benefit_down = forms.IntegerField(label='max_benefit_down', min_value=0, initial=1)
    order_total = forms.IntegerField(label='order_total', min_value=1, initial=1)
    order_same = forms.IntegerField(label='order_same', min_value=1, initial=1)
    data_type = forms.ChoiceField(label='data_type', choices=data_type_list)
    accepted_symbol_list = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=valid_symbol_list, initial=valid_symbol_list[0][0])
    output_format = forms.MultipleChoiceField(label='output_format', widget=forms.CheckboxSelectMultiple,
                                              choices=output_format_list, initial=output_format_list[0][0])
    strategy = forms.ChoiceField(label='strategy', choices=strategy_list, required=False)
    current_strategy_name = forms.CharField(label='current strategy name', required=False)
    strategy_variable = forms.CharField(label='strategy_variable', empty_value='', required=False, widget=forms.Textarea(attrs={'cols': 120, 'rows': 5}))
    strategy_context = forms.CharField(label='strategy_context', empty_value='', required=False, widget=forms.Textarea(attrs={'cols': 120, 'rows': 15}))

class OutPutForm0(forms.Form):
    time_frame_list = [('S1', 'S1'), ('M1', 'M1'), ('H1', 'H1'), ('D1', 'D1'), ('MN1', 'MN1'), ('Y1', 'Y1')]
    adjusted_mode_list = [(adjusted_mod_now_time, adjusted_mod_now_time)]
    adjusted_type = [(adjusted_type_all, 'سود + افزایش سرمایه'), (adjusted_type_capital_increase, 'افزایش سرمایه'),
                     (adjusted_type_take_profit, 'سود'), (adjusted_type_none, 'تعدیل نشده')]
    data_type_list = [(ts_data_type_open, 'open'), (ts_data_type_close, 'close'),
                      (ts_data_type_high, 'high'), (ts_data_type_low, 'low'),
                      (ts_data_type_weighted, 'weighted'), (ts_data_type_typical, 'typical'),
                      (ts_data_type_median, 'median')]

    db = Database(bt_database_info)

    # get date list -----------------
    valid_date_list = list()
    vdl, err = db.get_valid_date()

    try:
        for item in vdl:
            a = item[0] * 1000000
            s = str(item[1])
            b = s[0:4] + '/' + s[4:6] + '/' + s[6:] + ' : 00:00:00'
            valid_date_list.append((a, b))
    except:
        pass

    # get symbol list -----------------
    valid_symbol_list = list()
    symbol_list, err = db.get_symbols()  # en_symbol_12_digit_code, fa_symbol_30_digit_code, fa_symbol_name
    try:
        for item in symbol_list:
            a = item[0]
            b = str(item[1]) + ' (' + str(item[2]) + ')'
            valid_symbol_list.append((a, b))
    except:
        pass

    # strategy list -----------------
    strategy_list = [('-', 'not choice')]

    output_format_list = [('max_benefit', 'max_benefit'), ('back_test_benefit', 'back_test_benefit')]

    # -------------------

    start_date_time = forms.ChoiceField(label='زمان شروع:', choices=valid_date_list, widget=forms.HiddenInput())
    end_date_time = forms.ChoiceField(label='زمان پایان:', choices=valid_date_list, widget=forms.HiddenInput())
    time_frame = forms.ChoiceField(label='تایم فریم:', choices=time_frame_list, widget=forms.HiddenInput())
    adjusted_type = forms.ChoiceField(label='نوع تعدیل:', choices=adjusted_type, widget=forms.HiddenInput())
    max_benefit_up = forms.IntegerField(label='max_benefit_up', min_value=0, widget=forms.HiddenInput())
    max_benefit_down = forms.IntegerField(label='max_benefit_down', min_value=0, widget=forms.HiddenInput())
    order_total = forms.IntegerField(label='order_total', min_value=1, widget=forms.HiddenInput())
    order_same = forms.IntegerField(label='order_same', min_value=1, widget=forms.HiddenInput())
    data_type = forms.ChoiceField(label='data_type', choices=data_type_list, widget=forms.HiddenInput())
    strategy = forms.ChoiceField(label='strategy', choices=strategy_list, required=False, widget=forms.HiddenInput())
    current_strategy_name = forms.CharField(label='current strategy name', required=False, widget=forms.HiddenInput())

    accepted_symbol_list = forms.MultipleChoiceField(choices=valid_symbol_list, widget=forms.HiddenInput())
    output_format = forms.MultipleChoiceField(label='output_format', choices=output_format_list, widget=forms.HiddenInput())
    strategy_variable = forms.CharField(label='strategy_variable', empty_value='', required=False, widget=forms.HiddenInput())
    strategy_context = forms.CharField(label='strategy_context', empty_value='', required=False, widget=forms.HiddenInput())

class RecentResult(forms.Form):

    count = forms.IntegerField(label='count (1-10)', min_value=1, max_value=10)
