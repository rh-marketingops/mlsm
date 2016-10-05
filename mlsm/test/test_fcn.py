basic_fcn_good_fieldset = {
    'field1': int,
    'field2': str,
    'field3': float
}

def basic_fcn_good(data):
    return True

basic_fcn_add_fieldset = {
    'a': int,
    'b': int
}

def basic_fcn_add(data):
    a = data['a']
    b = data['b']
    c = a+b
    results = {'c': c}
    return results
