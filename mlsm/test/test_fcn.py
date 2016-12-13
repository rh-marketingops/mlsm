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

def basic_fcn_error(data, results):
    raise Exception('Hi! I am an error message')

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

############################################################
## Fcns for unit testing
############################################################

passes_intSingle_fieldset = {
    'a': int
}

def passes_intSingle(data, results):
    x = data['a'] + 1
    resultsReturn = {}
    resultsReturn['x'] = x
    return resultsReturn

passes_intMultiple_fieldset = {
    'a': int,
    'b': int
}

def passes_intMultiple(data, results):
    x = data['a'] + data['b']
    resultsReturn = {}
    resultsReturn['x'] = x
    return resultsReturn

fails_intSingle_fieldset = {
    'a': int
}

def fails_intSingle(data, results):
    x = data['a'] + 'lorem ipsum'
    resultsReturn = {}
    resultsReturn['x'] = x
    return resultsReturn

passes_strSingle_fieldset = {
    'a': str
}

def passes_strSingle(data, results):
    x = data['a'] + ' test'
    resultsReturn = {}
    resultsReturn['x'] = x
    return resultsReturn

passes_strMultiple_fieldset = {
    'a': str,
    'b': str
}

def passes_strMultiple(data, results):
    x = data['a'] + ' ' + data['b']
    resultsReturn = {}
    resultsReturn['x'] = x
    return resultsReturn

fails_strSingle_fieldset = {
    'a': str
}

def fails_strSingle(data, results):
    x = data['a'] + 1
    resultsReturn = {}
    resultsReturn['x'] = x
    return resultsReturn
