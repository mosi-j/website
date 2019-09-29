from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from copy import deepcopy
from .forms import InputParamsForm, RecentResult

from .bt_class.new_database import Database
from .bt_class.bt_setting import bt_database_info

from datetime import datetime, timedelta
import ast
from .bt_class.my_time import get_now_time_second

from .bt_class.test_strategy import TestStrategy

db = Database(bt_database_info)

# --------------------------
@login_required()
def back_test(request):
    print('back ----------------------')

    if request.method == 'POST':
        if request.POST['Btn_action'] == 'Submit':
            return add_order(request)

        #elif request.POST['Btn_action'] == 'Submit':
        #    return run(request)

        elif request.POST['Btn_action'] == 'load_strategy':
            return load_strategy(request)

        elif request.POST['Btn_action'] == 'update_strategy':
            return update_strategy(request)

        elif request.POST['Btn_action'] == 'save_strategy':
            return save_strategy(request)

        elif request.POST['Btn_action'] == 'test_strategy':
            return test_strategy(request)

        elif request.POST['Btn_action'] == 'back_to_run':
            return back_to_run(request)

        elif request.POST['Btn_action'] == 'select_all_symbol':
            return select_all_symbol(request)

        elif request.POST['Btn_action'] == 'reset_selected_symbol':
            return reset_selected_symbol(request)

    else:
        valid_strategy_list = get_strategy_list(request)
        form = InputParamsForm()
        form.fields['strategy'].choices += valid_strategy_list
        return render(request, 'back_test_app/input.html', {'form':form})

# --------------------------
@login_required()
def recent_result(request):
    print('--- recent back test result ----------------------')
    message = list()
    output = list()
    # print(request.POST)

    if request.method == 'POST':
        form = RecentResult(request.POST)
        if form.is_valid():
            # get recent result data
            res, err = db.get_back_test_result_data(request.user.username, form.cleaned_data['count'])
            # print(res)
            # print(err)
            if err is not None:
                message.append(err)
                #context = deepcopy(request.POST)
                print(request.POST)
                print(err)
                form = RecentResult(request.POST)
                return render(request, 'back_test_app/recent_result.html', {'form': form, 'output': output, 'message': message})
            if len(res) == 0:
                message.append('have not any data!')

            for item in res:
                item = list(item)
                # print(item)

                # start_run_date, run_time, params, outout
                try:
                    #var_list = ast.literal_eval(var_str)
                    opt_start_run_date = item[0]
                    opt_runtime = item[1]
                    opt_params = ast.literal_eval(item[2])
                    opt_result = ast.literal_eval(item[3])

                    output.append((opt_start_run_date, opt_runtime, opt_params, opt_result))

                except Exception as e:
                    print(e)

            # print(output)
            # create output data
            # context = deepcopy(request.POST)
            form = RecentResult(request.POST)
            return render(request, 'back_test_app/recent_result.html', {'form': form, 'output': output, 'message': message})

    else:
        form = RecentResult()
        return render(request, 'back_test_app/recent_result.html', {'form':form, 'output': output, 'message': message})

# --------------------------
def add_order(request):
    start_running_date = datetime.now()
    run_time = 0
    message = list()
    valid_strategy_list = get_strategy_list(request)

    form = InputParamsForm(request.POST)
    form.fields['strategy'].choices += valid_strategy_list
    # print(request.POST)
    # print(form.is_valid())
    if form.is_valid():
        strategy_context = form.cleaned_data['strategy_context']
        strategy_variable = form.cleaned_data['strategy_variable']

        # valid strategy
        res, err = run_test_strategy(strategy_variable, strategy_context)
        opt = list()

        if res is True:
            message.append('strategy is ok.')
            #from .bt_class.app import App

            start_date_time = int(form.cleaned_data['start_date_time'])
            end_date_time = int(form.cleaned_data['end_date_time'])
            time_frame = form.cleaned_data['time_frame']
            adjusted_type = int(form.cleaned_data['adjusted_type'])
            max_benefit_up = float(int(form.cleaned_data['max_benefit_up']) / 100)
            max_benefit_down = float(int(form.cleaned_data['max_benefit_down']) / 100)
            order_total = int(form.cleaned_data['order_total'])
            order_same = int(form.cleaned_data['order_same'])
            data_type = form.cleaned_data['data_type']
            output_format = form.cleaned_data['output_format']
            en_symbol_12_digit_code_list = form.cleaned_data['accepted_symbol_list']

            strategy = [strategy_variable, strategy_context]

            username = request.user.username
            order_id = username + ':' + str(int(get_now_time_second() % 1000000000))
            input_param = {'start_date_time':start_date_time, 'end_date_time':end_date_time, 'time_frame':time_frame, 'adjusted_type':adjusted_type, 'max_benefit_up':max_benefit_up, 'max_benefit_down':max_benefit_down, 'order_total':order_total, 'order_same':order_same, 'data_type':data_type, 'output_format':output_format, 'en_symbol_12_digit_code_list':en_symbol_12_digit_code_list, 'strategy':strategy}
            input_param = str(input_param)
            # add to waiting table
            res, err = db.add_order(order_id=order_id, username=username, input_param=input_param)
            if err is None:
                message.append('add order ok')
            else:
                message.append('add order fail: {0}'.format(err))

        else:
            message.append(err)

        # print(request.POST)
        context = deepcopy(request.POST)
        form = InputParamsForm(context)
        form.fields['strategy'].choices += valid_strategy_list

        return render(request, 'back_test_app/output.html', {'form': form, 'message': message, 'output':opt, 'run_time':run_time})

    message.append('form un valid')
    form = InputParamsForm()
    form.fields['strategy'].choices += valid_strategy_list
    return render(request, 'back_test_app/input.html', {'form': form, 'message': message})

def run(request):
    start_running_date = datetime.now()
    run_time = 0
    message = list()
    valid_strategy_list = get_strategy_list(request)

    form = InputParamsForm(request.POST)
    form.fields['strategy'].choices += valid_strategy_list
    # print(request.POST)
    # print(form.is_valid())
    if form.is_valid():
        strategy_context = form.cleaned_data['strategy_context']
        strategy_variable = form.cleaned_data['strategy_variable']

        # valid strategy
        res, err = run_test_strategy(strategy_variable, strategy_context)
        opt = list()

        if res is True:
            message.append('strategy is ok.')
            from .bt_class.app import App

            start_date_time = int(form.cleaned_data['start_date_time'])
            end_date_time = int(form.cleaned_data['end_date_time'])
            time_frame = form.cleaned_data['time_frame']
            adjusted_type = int(form.cleaned_data['adjusted_type'])
            max_benefit_up = float(int(form.cleaned_data['max_benefit_up']) / 100)
            max_benefit_down = float(int(form.cleaned_data['max_benefit_down']) / 100)
            order_total = int(form.cleaned_data['order_total'])
            order_same = int(form.cleaned_data['order_same'])
            data_type = form.cleaned_data['data_type']
            output_format = form.cleaned_data['output_format']
            en_symbol_12_digit_code_list = form.cleaned_data['accepted_symbol_list']

            strategy = [strategy_variable, strategy_context]
            app = App(strategy, output_format, start_date_time, end_date_time, time_frame, adjusted_type,
                      max_benefit_up, max_benefit_down, order_total, order_same, data_type)

            app.set_en_symbol_12_digit_code_list(en_symbol_12_digit_code_list)

            res = app.run(db)
            # opt.append(res)
            opt = res

            run_time = (datetime.now() - start_running_date).total_seconds()
            #params = str(form.cleaned_data)
            #output = str(opt)
            db.insert_back_test_result(username=request.user.username, start_run_date=str(start_runing_date),
                                       run_time=run_time, params=str(form.cleaned_data), outout=str(opt))

            message.append('run ok')
            #print(opt)

        else:
            message.append(err)

        # print(request.POST)
        context = deepcopy(request.POST)
        form = InputParamsForm(context)
        form.fields['strategy'].choices += valid_strategy_list

        return render(request, 'back_test_app/output.html', {'form': form, 'message': message, 'output':opt, 'run_time':run_time})

    message.append('form un valid')
    form = InputParamsForm()
    form.fields['strategy'].choices += valid_strategy_list
    return render(request, 'back_test_app/input.html', {'form': form, 'message': message})

def load_strategy(request):
    message = list()
    valid_strategy_list = get_strategy_list(request)

    form = InputParamsForm(request.POST)
    form.fields['strategy'].choices += valid_strategy_list

    if form.is_valid():
        strategy_name = request.POST['strategy']

        if request.POST['strategy'] != '-':
            strategy_data, err = db.get_strategy_context(request.user.username, strategy_name)
            if err is not None:
                message.append('load fault!')
                message.append(err)
                strategy_context = ''
                strategy_variable = ''
                current_strategy_name = ''
            else:
                message.append('load successful!')
                strategy_context = list(strategy_data[0])[0]
                strategy_variable = list(strategy_data[0])[1]
                current_strategy_name = strategy_name
        else:
            strategy_context = ''
            strategy_variable = ''
            current_strategy_name = ''
            message.append('please select valid strategy name')

        # print(request.POST)
        context = deepcopy(request.POST)
        context['strategy_context'] = strategy_context
        context['strategy_variable'] = strategy_variable
        context['current_strategy_name'] = current_strategy_name

        form = InputParamsForm(context)
        form.fields['strategy'].choices += valid_strategy_list
        return render(request, 'back_test_app/input.html', {'form': form, 'message': message})

    message.append('form un valid')
    form = InputParamsForm()
    form.fields['strategy'].choices += valid_strategy_list
    return render(request, 'back_test_app/input.html', {'form': form, 'message': message})

def update_strategy(request):
    message = list()
    valid_strategy_list = get_strategy_list(request)

    form = InputParamsForm(request.POST)
    form.fields['strategy'].choices += valid_strategy_list

    if form.is_valid():
        strategy_context = request.POST['strategy_context']
        strategy_variable = request.POST['strategy_variable']
        strategy_name = request.POST['strategy']

        res, err = db.update_strategy_context(request.user.username, strategy_name, strategy_variable, strategy_context)
        if err is not None:
            message.append('update fault!')
            message.append(err)
        else:
            message.append('update successful!')
        current_strategy_name = strategy_name

        context = deepcopy(request.POST)
        context['current_strategy_name'] = current_strategy_name

        form = InputParamsForm(context)
        form.fields['strategy'].choices += valid_strategy_list

        return render(request, 'back_test_app/input.html', {'form': form, 'message': message})

    message.append('form un valid')
    form = InputParamsForm()
    form.fields['strategy'].choices += valid_strategy_list
    return render(request, 'back_test_app/input.html', {'form': form, 'message': message})

def save_strategy(request):
    message = list()
    valid_strategy_list = get_strategy_list(request)

    form = InputParamsForm(request.POST)
    form.fields['strategy'].choices += valid_strategy_list
    # print(request.POST)
    # print(form.is_valid())
    if form.is_valid():
        strategy_context = request.POST['strategy_context']
        strategy_variable = request.POST['strategy_variable']
        strategy_name = request.POST['strategy']
        current_strategy_name = request.POST['current_strategy_name']
        # validation strategy_variable , strategy_context

        res, err = db.insert_strategy(request.user.username, current_strategy_name, strategy_variable, strategy_context)
        if err is not None:
            message.append('save fault!')
            message.append(err)
        else:
            message.append('save successful!')

        # print(request.POST)
        valid_strategy_list = get_strategy_list(request)
        context = deepcopy(request.POST)
        context['strategy'] = current_strategy_name
        form = InputParamsForm(context)
        form.fields['strategy'].choices += valid_strategy_list

        return render(request, 'back_test_app/input.html', {'form': form, 'message': message})

    message.append('form un valid')
    form = InputParamsForm()
    form.fields['strategy'].choices += valid_strategy_list
    return render(request, 'back_test_app/input.html', {'form': form, 'message': message})

def test_strategy(request):
    message = list()
    print(request.POST)
    valid_strategy_list = get_strategy_list(request)

    form = InputParamsForm(request.POST)
    form.fields['strategy'].choices += valid_strategy_list
    if form.is_valid():
        current_strategy_name = form.cleaned_data['current_strategy_name']
        # ------------------------------------------------------------
        strategy_context = form.cleaned_data['strategy_context']
        strategy_variable = form.cleaned_data['strategy_variable']

        print('start--------------------------------')
        res, err = run_test_strategy(strategy_variable, strategy_context)
        if res is True:
            message.append('strategy is ok.')
        else:
            message.append(err)

        context = deepcopy(request.POST)
        context['strategy'] = current_strategy_name
        form = InputParamsForm(context)
        form.fields['strategy'].choices += valid_strategy_list

        return render(request, 'back_test_app/input.html', {'form': form, 'message': message})

    message.append('form un valid')
    form = InputParamsForm()
    form.fields['strategy'].choices += valid_strategy_list
    return render(request, 'back_test_app/input.html', {'form': form, 'message': message})

def get_strategy_list(request):
    valid_strategy_list = list()
    strategy_list, err = db.get_strategy_name_list(request.user.username)
    try:
        for item in strategy_list:
            a = item[0]
            valid_strategy_list.append((a, a))
    except Exception as e:
        print(str(e))
        valid_strategy_list = list()
        return valid_strategy_list

    return valid_strategy_list

def back_to_run(request):
    message = list()
    valid_strategy_list = get_strategy_list(request)

    form = InputParamsForm(request.POST)
    form.fields['strategy'].choices += valid_strategy_list

    if form.is_valid():
        context = deepcopy(request.POST)

        form = InputParamsForm(context)
        form.fields['strategy'].choices += valid_strategy_list
        return render(request, 'back_test_app/input.html', {'form': form, 'message': message})

    message.append('form un valid')
    form = InputParamsForm()
    form.fields['strategy'].choices += valid_strategy_list
    return render(request, 'back_test_app/input.html', {'form': form, 'message': message})

def select_all_symbol(request):
    message = list()
    valid_strategy_list = get_strategy_list(request)

    form = InputParamsForm(request.POST)
    form.fields['strategy'].choices += valid_strategy_list

    #print(request.POST)
    if form.is_valid():

        symbols = form.fields['accepted_symbol_list'].choices
        all_symbol = list()
        for item in symbols:
            all_symbol.append(item[0])

        form.cleaned_data['accepted_symbol_list'] = all_symbol
        context = deepcopy(form.cleaned_data)

        form = InputParamsForm(context)
        form.fields['strategy'].choices += valid_strategy_list

        return render(request, 'back_test_app/input.html', {'form': form, 'message': message})

    message.append('form un valid')
    form = InputParamsForm()
    form.fields['strategy'].choices += valid_strategy_list
    return render(request, 'back_test_app/input.html', {'form': form, 'message': message})

def reset_selected_symbol(request):
    message = list()
    valid_strategy_list = get_strategy_list(request)

    form = InputParamsForm(request.POST)
    form.fields['strategy'].choices += valid_strategy_list

    # print(request.POST)
    if form.is_valid():

        form.cleaned_data['accepted_symbol_list'] = []
        context = deepcopy(form.cleaned_data)

        form = InputParamsForm(context)
        form.fields['strategy'].choices += valid_strategy_list

        return render(request, 'back_test_app/input.html', {'form': form, 'message': message})

    message.append('form un valid')
    form = InputParamsForm()
    form.fields['strategy'].choices += valid_strategy_list
    return render(request, 'back_test_app/input.html', {'form': form, 'message': message})

# --------------------------
def run_test_strategy(strategy_variable, strategy_context):

    ts = TestStrategy()
    res = ts.run_strategy(strategy_variable=strategy_variable, strategy_context=strategy_context)

    if res is None:
        return True, None
    else:
        return False, res

def run_test_strategy1(strategy_variable, strategy_context):

    ts = TestStrategy()
    ts.run_strategy(strategy_variable=strategy_variable, strategy_context=strategy_context)



    from .bt_class.app import App
    from .bt_class.constant import ts_data_type_close, adjusted_type_all


    start_date_time = 20190703122000
    end_date_time = 20190703122900
    time_frame = 'M1'
    adjusted_type = adjusted_type_all
    max_benefit_up = 0.1
    max_benefit_down = 0.05
    order_total = 3
    order_same = 2
    data_type = ts_data_type_close
    output_format = None
    en_symbol_12_digit_code_list = ['IRO3PMRZ0001']
    strategy = [strategy_variable, strategy_context]

    # run analize app
    app = App(strategy, output_format, start_date_time, end_date_time, time_frame, adjusted_type,
              max_benefit_up, max_benefit_down, order_total, order_same, data_type)

    app.set_en_symbol_12_digit_code_list(en_symbol_12_digit_code_list)

    res, err = app.test_strategy()

    if res is True:
        return True, None
    else:
        return False, err

# --------------------------
