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
    resultsReturn = {}
    resultsReturn['c'] = c
    return resultsReturn

def basic_sum_fcn(data, results):
    x = results['test']['0.0.0']['c']
    y = x + 5
    resultsReturn = {}
    resultsReturn['d'] = y
    return resultsReturn

def basic_sum_fcn_multiple(data, results):
    x1 = results['test1']['0.0.0']['c']
    x2 = results['test2']['0.0.0']['c']
    x3 = results['test3']['0.0.0']['c']
    y = x1+x2+x3
    resultsReturn = {}
    resultsReturn['d'] = y
    return resultsReturn
