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
    x = results['test']['results']['c']
    y = x + 5
    results['d'] = y
    return results

def basic_sum_fcn_multiple(data, results):
    x1 = results['test1']['results']['c']
    x2 = results['test2']['results']['c']
    x3 = results['test3']['results']['c']
    y = x1+x2+x3
    results['d'] = y
    return results
