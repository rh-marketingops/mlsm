basic_fcn_good_fieldset = {
    'field1': int,
    'field2': str,
    'field3': float
}

def basic_fcn_good(data, results):
    return True

basic_fcn_add_fieldset = {
    'a': int,
    'b': int
}

def basic_fcn_add(data, results):
    a = data['a']
    b = data['b']
    c = a+b
    results['c'] = c
    return results

def basic_fcn_add_useresults(data, results):
    a = data['a']
    b = data['b']
    c = results['test']['c']
    d = a+b+c
    results['d'] = d
    return results

def basic_sum_fcn(data, results):
    return True
