###############################################################################
## imports
###############################################################################

import mongomock
import time
from nose.tools import *
from mock import patch

import mlsm

from . import test_fcn

###############################################################################
## setup test db
###############################################################################

db = mongomock.MongoClient().db

###############################################################################
## setup basic config
###############################################################################

version = '0.0.0'

###############################################################################
## Test Definitions
###############################################################################

# create model check name
def test_createNewModelCheckName():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_good_fieldset, version=version, fcn = test_fcn.basic_fcn_good)
    assert testmodel.name == 'test'

# create model check field listing
def test_createNewModelCheckFields():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_good_fieldset, version=version, fcn = test_fcn.basic_fcn_good)
    assert testmodel.fields == test_fcn.basic_fcn_good_fieldset

# create model check function
def test_createNewModelCheckFcn():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_good_fieldset, version=version, fcn = test_fcn.basic_fcn_good)
    assert testmodel.fcn == test_fcn.basic_fcn_good

# create model check version
def test_createNewModelCheckVersion():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_good_fieldset, version=version, fcn = test_fcn.basic_fcn_good)
    assert testmodel.version == version

# create model check basic fcn True
def test_createNewModelCheckBasicFcn():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_good_fieldset, version=version, fcn = test_fcn.basic_fcn_good)
    assert testmodel.fcn(data={})

# basic addition model
def test_createNewModelCheckAddFcn():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    results = testmodel.fcn(data={'a': 1, 'b': 2})
    assert results['c'] == 3

def test_createNewModelRun():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    results = testmodel.execute(data={'a': 1, 'b': 2})
    assert results['c'] == 3

@raises()
def test_createNewModelRun():
    testmodel = mlsm.Model(name='test', fields=test_fcn.basic_fcn_add_fieldset, version=version, fcn = test_fcn.basic_fcn_add)
    results = testmodel.execute(data={'a': 1, 'b': 2, 'd': 3})
    assert results['c'] == 3
